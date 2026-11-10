"""Claude API 공통 헬퍼."""
import os

from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = "claude-sonnet-5-5"


def get_client():
    """ANTHROPIC_API_KEY 를 읽어 Anthropic 클라이언트를 만든다."""
    from anthropic import Anthropic

    if not os.getenv("ANTHROPIC_API_KEY"):
        raise RuntimeError(
            "ANTHROPIC_API_KEY 가 없습니다. .env 파일이나 환경 시크릿에 설정하세요."
        )
    return Anthropic()


def get_model() -> str:
    return os.getenv("CLAUDE_MODEL") or DEFAULT_MODEL


def ask(system: str, messages: list[dict], max_tokens: int = 2000) -> str:
    """시스템 프롬프트와 대화 목록을 보내고 텍스트 답변을 돌려준다."""
    client = get_client()
    resp = client.messages.create(
        model=get_model(),
        max_tokens=max_tokens,
        system=system,
        messages=messages,
    )
    return "".join(b.text for b in resp.content if b.type == "text")
