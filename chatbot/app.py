"""해운·철강 업무용 챗봇 웹페이지 (Streamlit).

실행:
  streamlit run chatbot/app.py
브라우저에서 http://localhost:8501 접속
"""
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common.llm import ask  # noqa: E402

SYSTEM = """당신은 해운·철강 물류 실무를 돕는 한국어 업무 비서입니다.
- 분야: 벌크/철강재 해상운송, 용선(Chartering), Fixture, Laycan, Demurrage/Despatch,
  NOR, B/L, 운임 협상, 한국·중국·일본·대만·베트남·동남아 항로.
- 답변은 핵심 요약을 먼저, 그다음 짧은 항목별 설명.
- 모르는 것은 모른다고 말하고, 숫자·날짜·시장 운임을 지어내지 마세요.
- 영어·일본어·베트남어 메일 초안 요청 시 해당 언어로 작성하고, 한국어 설명을 짧게 덧붙이세요.
"""

QUICK = {
    "📧 영문 메일 초안": "다음 내용을 정중한 영문 메일로 써줘: ",
    "📘 용어 설명": "다음 해운 용어를 쉽게 설명해줘: ",
    "⏱️ 체선료 계산": "다음 조건으로 Demurrage/Despatch를 계산해줘 (계산 과정 포함): ",
}

st.set_page_config(page_title="Shipping Assistant", page_icon="🚢")
st.title("🚢 해운·철강 업무 챗봇")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.subheader("빠른 시작")
    for label, prefix in QUICK.items():
        if st.button(label, use_container_width=True):
            st.session_state.prefill = prefix
    if st.button("🗑️ 대화 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    if prefill := st.session_state.get("prefill"):
        st.info(f"입력창에 이어서 쓰세요:\n\n`{prefill}`")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("무엇을 도와드릴까요?"):
    if prefill := st.session_state.pop("prefill", None):
        prompt = prefill + prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("생각 중..."):
            try:
                answer = ask(SYSTEM, st.session_state.messages)
            except Exception as e:  # API 키 누락 등
                answer = f"⚠️ 오류: {e}"
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
