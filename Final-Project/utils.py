"""검색 근거 검증과 추천 결과 구성에 사용하는 보조 함수."""

import re

from models import GameEvidence, Request

TAG_WORDS = {
    "협동": r"\bco[ -]?op(?:erative)?\b|협동",
    "생존": r"\bsurviv(?:al|e)\b|생존",
    "파티": r"\bparty\b|파티",
    "전략": r"\bstrateg(?:y|ic)\b|전략",
    "퍼즐": r"\bpuzzle\b|퍼즐",
    "액션": r"\baction\b|액션",
    "RPG": r"\b(?:[aj]?rpg|role[ -]?playing)\b|롤\s*플레잉",
    "시뮬레이션": r"\bsimulat(?:ion|or)\b|시뮬레이션|시뮬레이터",
    "어드벤처": r"\badventure\b|어드벤처|모험",
    "공포": r"\bhorror\b|공포",
}
ONLINE_WORDS = r"\bonline\b|온라인"
LOCAL_WORDS = r"\blocal\b|\blan\b|\boffline\b|\bsplit[ -]?screen\b|로컬|오프라인|화면\s*분할"
NEGATED_HORROR = re.compile(
    r"(?i)\b(?:no|without|not(?:\s+a)?)\s+horror\b|\bhorror[ -]free\b|비\s*공포"
    r"|공포\s*(?:요소가?|장면이?)?\s*(?:없는|없음|없습니다)"
)
RANGE = re.compile(
    r"(?i)(?<!\d)(\d{1,2})\s*(?:players?|people|명|인)?\s*"
    r"(?:-|–|~|to|부터|에서)\s*(\d{1,2})\s*(?:players?|people|명|인)"
)

def _normalized(value: str) -> str:
    return " ".join(value.split()).casefold()


def _verified_quote(quote: str | None, source: str) -> str | None:
    if not isinstance(quote, str) or not 2 <= len(quote) <= 300 or "|" in quote:
        return None
    return quote if _normalized(quote) in _normalized(source) else None


def apply_evidence(game: dict, evidence: GameEvidence | None) -> dict:
    """모델이 제시한 근거가 원문에 있고 조건에 맞는지 확인한다."""
    result = {**game, "players": None, "player_quote": None, "tags": set()}
    if evidence is None or evidence.app_id != game["app_id"]:
        return result
    quote = _verified_quote(evidence.player_quote, game["source"])
    if quote:
        for sentence in re.split(r"(?<=[.!?])\s+", quote):
            match = RANGE.search(sentence)
            if match and re.search(ONLINE_WORDS, sentence, re.I) and not re.search(LOCAL_WORDS, sentence, re.I):
                low, high = map(int, match.groups())
                if 1 <= low <= high <= 100:
                    result["players"] = (low, high)
                    result["player_quote"] = sentence
                    break
    for tag in evidence.tags:
        quote = _verified_quote(tag.quote, game["source"])
        if quote and re.search(TAG_WORDS[tag.tag], quote, re.I):
            # 부정 문구에서 잘려 나온 단어도 공포 장르의 근거가 아니다.
            if tag.tag == "공포" and NEGATED_HORROR.search(game["source"]):
                continue
            result["tags"].add(tag.tag)
    return result


def rank_games(games: list[dict], request: Request) -> list[dict]:
    """필수 조건을 검사하고 확인 여부와 참가자 취향에 따라 정렬한다."""
    ranked = []
    solo = request["players"] == 1
    for game in games:
        if not solo and game["online"] is False:
            continue
        if game["price"] is not None and game["price"] > request["budget"]:
            continue
        if not solo and game["players"] and not game["players"][0] <= request["players"] <= game["players"][1]:
            continue
        missing = []
        if solo:
            if game.get("singleplayer") is not True:
                missing.append("1인 플레이")
        else:
            if game["online"] is not True:
                missing.append("온라인 멀티플레이")
            if game["players"] is None:
                missing.append("함께 플레이할 수 있는 인원")
        if game["released"] is not True:
            missing.append("출시 여부")
        if game["price"] is None:
            missing.append("한국 가격")
        preferences = {p["preference"] for p in request["participants"]}
        score = sum(p["preference"] in game["tags"] for p in request["participants"])
        ranked.append({**game, "solo": solo, "missing": missing, "score": score, "matched_tags": game["tags"] & preferences})
    return sorted(ranked, key=lambda game: (bool(game["missing"]), -game["score"], game["name"].casefold()))[:3]


def _escape(text: str) -> str:
    text = " ".join(text.split())
    return re.sub(r"([\\`*_{}\[\]()<>#@|~])", r"\\\1", text)


def format_result(games: list[dict], notice: str = "") -> str:
    """추천 후보와 미확인 조건을 디스코드 메시지로 만든다."""
    if not games:
        if notice:
            return notice + "\n추천할 게임을 표시하지 못했습니다. 조건과 연결 상태를 확인하고 다시 시도해 주세요."
        return "이번 검색에서 조건에 맞는 스팀 게임을 찾지 못했습니다. 조건을 바꿔 다시 검색해 주세요."
    lines = [notice] if notice else []
    for index, game in enumerate(games, 1):
        status = "확인 필요" if game["missing"] else "조건 확인"
        lines.append(f"\n**{index}. {_escape(game['name'][:80])} — {status}**")
        price = "미확인" if game["price"] is None else f"{game['price']:,}원"
        if game["solo"]:
            players = "가능" if game.get("singleplayer") is True else "미확인"
            lines.append(f"가격: {price} | 1인 플레이: {players}")
        else:
            players = "미확인" if game["players"] is None else f"{game['players'][0]}~{game['players'][1]}명"
            lines.append(f"가격: {price} | 온라인 인원: {players}")
        if game["matched_tags"]:
            lines.append("일치한 취향: " + ", ".join(sorted(game["matched_tags"])))
        if game["missing"]:
            lines.append("직접 확인: " + ", ".join(game["missing"]))
        if not game["solo"] and game["player_quote"]:
            lines.append("인원 근거: " + _escape(game["player_quote"][:80]))
        lines.append(f"[스팀 상점]({game['url']}) · 확인: {game['checked_at']}")
    lines.append("\n가격과 지원 방식은 구매 전에 스팀 상점에서 다시 확인해 주세요.")
    return "\n".join(lines)

