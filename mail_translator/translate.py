"""해운·철강 업무 메일 번역기.

사용 예:
  # 한→영: Formal / Neutral / Casual 3가지 버전
  python -m mail_translator.translate ko2en "선적 일정이 2일 지연될 예정입니다."

  # 영→한: 번역 + 핵심 요약 + 조치 사항
  python -m mail_translator.translate en2ko -f incoming_mail.txt

  # 표준입력도 가능
  cat mail.txt | python -m mail_translator.translate en2ko
"""
import argparse
import sys

from common.llm import ask

DOMAIN = (
    "You are an expert in dry bulk / steel shipping (chartering, fixtures, "
    "laycan, demurrage, NOR, B/L, freight rates) between Korea, China, Japan, "
    "Taiwan, Vietnam and Southeast Asia. Keep industry terms and abbreviations "
    "accurate (e.g. laycan, NOR, SHINC, PWWD, CQD, BL, MT, USD/MT). "
    "Never invent figures, dates, vessel names or terms that are not in the source."
)

KO2EN_SYSTEM = DOMAIN + """
Translate the Korean business text into English in THREE styles.
Output exactly this format in Markdown:

### Formal
<text>

### Neutral
<text>

### Casual
<text>

### Notes
- (one or two short notes in Korean about term choices or ambiguous points; write '- 없음' if none)
"""

EN2KO_SYSTEM = DOMAIN + """
The user gives an English business email/chat. Respond in Korean, exactly in this Markdown format:

### 핵심 요약
- (3줄 이내)

### 조치 필요 사항
- (상대가 요청한 것, 기한 포함. 없으면 '- 없음')

### 주요 조건
- (선명, 화물, 수량, laycan, 운임, 항구 등 메일에 있는 것만. 없으면 '- 없음')

### 전체 번역
<자연스러운 한국어 번역>
"""


def translate(mode: str, text: str) -> str:
    system = KO2EN_SYSTEM if mode == "ko2en" else EN2KO_SYSTEM
    return ask(system, [{"role": "user", "content": text}])


def main() -> None:
    p = argparse.ArgumentParser(description="해운·철강 업무 메일 번역기")
    p.add_argument("mode", choices=["ko2en", "en2ko"], help="번역 방향")
    p.add_argument("text", nargs="?", help="번역할 문장 (생략 시 -f 또는 표준입력)")
    p.add_argument("-f", "--file", help="번역할 텍스트 파일 경로")
    args = p.parse_args()

    if args.text:
        text = args.text
    elif args.file:
        with open(args.file, encoding="utf-8") as fh:
            text = fh.read()
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        p.error("번역할 문장, -f 파일, 또는 표준입력 중 하나가 필요합니다.")

    if not text.strip():
        p.error("입력이 비어 있습니다.")

    try:
        print(translate(args.mode, text))
    except RuntimeError as e:
        sys.exit(f"❌ {e}")


if __name__ == "__main__":
    main()
