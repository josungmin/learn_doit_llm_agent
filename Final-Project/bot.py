import asyncio
import logging
import os
from pathlib import Path

import discord
from discord import app_commands
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from models import Preference
from recommender import build_graph
from sessions import SessionError, Sessions

logger = logging.getLogger(__name__)


class GameBot(discord.Client):
    def __init__(self, guild_id: int, graph):
        super().__init__(intents=discord.Intents.default(), allowed_mentions=discord.AllowedMentions.none())
        self.guild_id = guild_id
        self.graph = graph
        self.sessions = Sessions()
        self.locks: dict[tuple[int, int], asyncio.Lock] = {}
        self.tree = app_commands.CommandTree(self)
        self.register_commands()

    async def setup_hook(self):
        guild = discord.Object(id=self.guild_id)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

    def lock_for(self, key: tuple[int, int]) -> asyncio.Lock:
        return self.locks.setdefault(key, asyncio.Lock())

    def register_commands(self):
        @self.tree.command(name="게임시작", description="스팀 게임 찾기를 시작합니다.")
        @app_commands.describe(인원="플레이할 인원 (1~10명)", 예산="한 사람당 최대 예산 (원, 0은 무료)")
        async def start(interaction: discord.Interaction, 인원: app_commands.Range[int, 1, 10], 예산: int):
            key = (interaction.guild_id, interaction.channel_id)
            async with self.lock_for(key):
                try:
                    self.sessions.start(key, interaction.user.id, 인원, 예산)
                    message = f"{인원}명이 참여할 게임 찾기를 시작합니다. 방장도 /게임참여로 참여해 주세요."
                    private = False
                except SessionError as exc:
                    message, private = str(exc), True
            await interaction.response.send_message(message, ephemeral=private)

        @self.tree.command(name="게임참여", description="선호하는 게임 유형을 입력합니다.")
        @app_commands.describe(선호="좋아하는 게임 유형")
        async def join(interaction: discord.Interaction, 선호: Preference):
            key = (interaction.guild_id, interaction.channel_id)
            async with self.lock_for(key):
                try:
                    session = self.sessions.join(key, interaction.user.id, 선호)
                    message = f"참가 정보를 저장했습니다. 현재 {len(session.participants)}/{session.players}명입니다."
                except SessionError as exc:
                    message = str(exc)
            await interaction.response.send_message(message, ephemeral=True)

        @self.tree.command(name="게임나가기", description="현재 게임 찾기에서 나갑니다.")
        async def leave(interaction: discord.Interaction):
            key = (interaction.guild_id, interaction.channel_id)
            async with self.lock_for(key):
                try:
                    self.sessions.leave(key, interaction.user.id)
                    message = "모임에서 나갔습니다."
                except SessionError as exc:
                    message = str(exc)
            await interaction.response.send_message(message, ephemeral=True)

        @self.tree.command(name="게임종료", description="방장이 현재 게임 찾기를 종료합니다.")
        async def end(interaction: discord.Interaction):
            key = (interaction.guild_id, interaction.channel_id)
            async with self.lock_for(key):
                try:
                    self.sessions.end(key, interaction.user.id)
                    message, private = "게임 찾기를 종료하고 참가 정보를 삭제했습니다.", False
                except SessionError as exc:
                    message, private = str(exc), True
            await interaction.response.send_message(message, ephemeral=private)

        @self.tree.command(name="게임추천", description="방장이 참가자 조건에 맞는 스팀 게임을 찾습니다.")
        async def recommend(interaction: discord.Interaction):
            key = (interaction.guild_id, interaction.channel_id)
            async with self.lock_for(key):
                try:
                    session, revision, snapshot = self.sessions.begin_search(key, interaction.user.id)
                except SessionError as exc:
                    message = str(exc)
                else:
                    message = None
            if message:
                await interaction.response.send_message(message, ephemeral=True)
                return
            try:
                await interaction.response.defer(thinking=True)
                state = await asyncio.wait_for(self.graph.ainvoke({"request": snapshot}), timeout=120)
                message = state["result"]
            except asyncio.CancelledError:
                async with self.lock_for(key):
                    self.sessions.finish_search(key, session, revision)
                raise
            except asyncio.TimeoutError:
                message = "검색 시간이 초과되었습니다. 잠시 후 다시 시도해 주세요."
            except Exception as exc:
                logger.warning("추천 실패: %s", type(exc).__name__)
                message = "게임을 찾는 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요."
            async with self.lock_for(key):
                if not self.sessions.finish_search(key, session, revision):
                    message = "추천 중 참가 정보가 바뀌거나 모임이 종료되었습니다. 다시 요청해 주세요."
                if interaction.response.is_done():
                    await interaction.edit_original_response(content=message)
                else:
                    await interaction.response.send_message(message, ephemeral=True)

    async def on_ready(self):
        logger.info("디스코드 봇이 준비되었습니다.")


def main():
    load_dotenv(Path(__file__).with_name(".env"))
    token = os.getenv("DISCORD_BOT_TOKEN", "").strip()
    guild_id = os.getenv("DISCORD_GUILD_ID", "").strip()
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not token or not guild_id.isdecimal() or int(guild_id) <= 0 or not api_key:
        raise SystemExit(".env에 DISCORD_BOT_TOKEN, 숫자 DISCORD_GUILD_ID, OPENAI_API_KEY를 설정해 주세요.")
    model_name = os.getenv("OPENAI_MODEL", "").strip() or "gpt-5.4-mini"
    model = ChatOpenAI(model=model_name, api_key=api_key, timeout=45, max_retries=0)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    GameBot(int(guild_id), build_graph(model)).run(token, log_handler=None)


if __name__ == "__main__":
    main()
