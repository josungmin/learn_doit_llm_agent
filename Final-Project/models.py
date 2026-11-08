"""참가 조건과 모델이 추출하는 근거의 구조를 정의한다."""

from typing import Literal, TypedDict

from pydantic import BaseModel, ConfigDict

Genre = Literal["협동", "생존", "파티", "전략", "퍼즐", "액션", "RPG", "시뮬레이션", "어드벤처", "공포"]
Preference = Literal[Genre, "상관없음"]


class Participant(TypedDict):
    preference: Preference


class Request(TypedDict):
    players: int
    budget: int
    participants: list[Participant]


class TagEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid")
    tag: Genre
    quote: str


class GameEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid")
    app_id: str
    player_quote: str | None
    tags: list[TagEvidence]


class EvidenceList(BaseModel):
    model_config = ConfigDict(extra="forbid")
    games: list[GameEvidence]
