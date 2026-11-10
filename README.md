# Owner
해운·철강 업무를 돕는 AI 도구 모음입니다.

| 폴더 | 도구 | API 키 필요 |
|---|---|---|
| `mail_translator/` | 📧 업무 메일 번역기 (한→영 3가지 스타일, 영→한 요약) | ✅ |
| `freight_analysis/` | 🚢 운임(Fixture) 데이터 분석 + 차트 | ❌ |
| `chatbot/` | 💬 해운·철강 업무 챗봇 웹페이지 | ✅ |

## 1. 설치
```bash
bash scripts/setup.sh
cp .env.example .env      # 그리고 .env 에 ANTHROPIC_API_KEY 입력
```
> ⚠️ 이 저장소는 공개(public)입니다. API 키는 `.env`나 환경 시크릿에만 넣고 절대 커밋하지 마세요.

## 2. 메일 번역기
```bash
# 한→영: Formal / Neutral / Casual
python -m mail_translator.translate ko2en "선적 일정이 2일 지연될 예정입니다. 양해 부탁드립니다."

# 영→한: 핵심 요약 + 조치 사항 + 주요 조건 + 전체 번역
python -m mail_translator.translate en2ko -f incoming_mail.txt
```

## 3. 운임 데이터 분석
```bash
python -m freight_analysis.analyze                         # 샘플 데이터
python -m freight_analysis.analyze my_fixtures.csv         # 내 데이터
python -m freight_analysis.analyze my.csv --route "Pohang-Shanghai"
```
- CSV 필수 컬럼: `date, route, cargo, quantity_mt, rate_usd_mt`
- 결과: `output/report.md`, `output/route_summary.csv`, `output/monthly_trend.png`
- ⚠️ `sample_data/`의 데이터는 **테스트용 가짜 데이터**이며 실제 시장 운임이 아닙니다.

## 4. 업무 챗봇
```bash
streamlit run chatbot/app.py
```
브라우저에서 `http://localhost:8501` 접속.

## 클라우드 환경 설정 (Claude Code)
- **설정 스크립트**: `bash scripts/setup.sh`
- **네트워크**: 기본(Trusted) + `api.anthropic.com`
- **시크릿**: `ANTHROPIC_API_KEY`
- **변수**: `TZ=Asia/Seoul`, `PYTHONUNBUFFERED=1`, (선택) `CLAUDE_MODEL`
