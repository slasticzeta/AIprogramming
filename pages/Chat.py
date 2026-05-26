import streamlit as st
from openai import OpenAI

# ── 페이지 설정 ──────────────────────────────────────────
st.set_page_config(page_title="Chat", page_icon="💬")
st.title("💬 Chat")

# ── session_state 초기화 ─────────────────────────────────
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── 사이드바: API Key 입력 + Clear 버튼 ──────────────────
with st.sidebar:
    st.header("🔑 API Key 설정")
    input_key = st.text_input(
        "OpenAI API Key를 입력하세요",
        type="password",
        value=st.session_state.api_key,
        placeholder="sk-...",
    )
    if input_key:
        st.session_state.api_key = input_key
        st.success("API Key가 저장되었습니다 ✅")
    else:
        st.warning("API Key를 입력해주세요")

    st.divider()

    # Clear 버튼: 대화 내용 초기화
    if st.button("🗑️ Clear 대화 초기화", type="secondary", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ── 기존 대화 내용 출력 ───────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ── 사용자 입력 ───────────────────────────────────────────
user_input = st.chat_input("메시지를 입력하세요...")

if user_input:
    if not st.session_state.api_key:
        st.error("❌ 왼쪽 사이드바에서 API Key를 먼저 입력해주세요.")
    else:
        # 사용자 메시지 저장 & 출력
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # LLM 응답 생성
        with st.chat_message("assistant"):
            with st.spinner("답변 생성 중..."):
                try:
                    client = OpenAI(api_key=st.session_state.api_key)
                    response = client.chat.completions.create(
                        model="gpt-5.4-mini",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant. Answer in Korean."},
                            *st.session_state.messages,
                        ],
                    )
                    answer = response.choices[0].message.content
                    st.write(answer)
                    # assistant 응답 저장
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")
