from dataclasses import dataclass, field
from typing import get_args

from models import Preference


class SessionError(ValueError):
    pass


@dataclass
class Session:
    host_id: int
    players: int
    budget: int
    participants: dict[int, dict[str, str]] = field(default_factory=dict)
    revision: int = 0
    searching: bool = False


class Sessions:
    def __init__(self):
        self.items: dict[tuple[int, int], Session] = {}

    def get(self, key: tuple[int, int]) -> Session:
        session = self.items.get(key)
        if session is None:
            raise SessionError("진행 중인 모임이 없습니다. /게임시작으로 먼저 시작해 주세요.")
        return session

    def start(self, key: tuple[int, int], host_id: int, players: int, budget: int) -> Session:
        if key in self.items:
            raise SessionError("이 채널에 진행 중인 모임이 있습니다. 방장이 먼저 종료해 주세요.")
        if not 1 <= players <= 10 or budget < 0:
            raise SessionError("인원은 1~10명, 예산은 0원 이상으로 입력해 주세요.")
        session = Session(host_id, players, budget)
        self.items[key] = session
        return session

    def join(self, key: tuple[int, int], user_id: int, preference: str) -> Session:
        session = self.get(key)
        if preference not in get_args(Preference):
            raise SessionError("제공된 선호 장르 중에서 선택해 주세요.")
        if user_id not in session.participants and len(session.participants) >= session.players:
            raise SessionError("참가 인원이 가득 찼습니다.")
        session.participants[user_id] = {"preference": preference}
        session.revision += 1
        return session

    def leave(self, key: tuple[int, int], user_id: int) -> Session:
        session = self.get(key)
        if user_id not in session.participants:
            raise SessionError("참가 중인 모임이 아닙니다.")
        del session.participants[user_id]
        session.revision += 1
        return session

    def begin_search(self, key: tuple[int, int], user_id: int) -> tuple[Session, int, dict]:
        session = self.get(key)
        if session.host_id != user_id:
            raise SessionError("게임 추천은 모임을 시작한 방장만 요청할 수 있습니다.")
        if len(session.participants) != session.players:
            raise SessionError(f"참가자를 기다리는 중입니다. ({len(session.participants)}/{session.players}명)")
        if session.searching:
            raise SessionError("이미 게임을 찾고 있습니다. 잠시만 기다려 주세요.")
        session.searching = True
        snapshot = {
            "players": session.players,
            "budget": session.budget,
            "participants": [dict(p) for p in session.participants.values()],
        }
        return session, session.revision, snapshot

    def finish_search(self, key: tuple[int, int], session: Session, revision: int) -> bool:
        if self.items.get(key) is not session:
            return False
        session.searching = False
        return session.revision == revision

    def end(self, key: tuple[int, int], user_id: int) -> None:
        session = self.get(key)
        if session.host_id != user_id:
            raise SessionError("모임은 방장만 종료할 수 있습니다.")
        del self.items[key]
