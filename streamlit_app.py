import streamlit as st
from openai import OpenAI

# ── 페이지 설정 ──────────────────────────────────────────
st.set_page_config(page_title="LLM 챗봇", page_icon="🤖")
st.title("🤖 LLM 응답 웹앱")

# ── session_state 초기화 ─────────────────────────────────
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# ── 사이드바: API Key 입력 ────────────────────────────────
with st.sidebar:
    st.header("🔑 API Key 설정")
    input_key = st.text_input(
        "OpenAI API Key를 입력하세요",
        type="password",
        value=st.session_state.api_key,
        placeholder="sk-...",
    )
    # 입력값을 session_state에 저장 (페이지 이동 후 돌아와도 유지)
    if input_key:
        st.session_state.api_key = input_key
        st.success("API Key가 저장되었습니다 ✅")
    else:
        st.warning("API Key를 입력해주세요")

# ── LLM 호출 함수 (@st.cache_data: 동일 입력이면 캐시 반환) ──
@st.cache_data
def get_llm_response(api_key: str, user_question: str) -> str:
    """동일한 api_key + user_question 조합이면 캐시된 결과를 반환합니다."""
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Answer in Korean."},
            {"role": "user",   "content": user_question},
        ],
    )
    return response.choices[0].message.content

# ── 메인 화면: 질문 입력 & 응답 출력 ─────────────────────
st.subheader("💬 질문을 입력하세요")
user_question = st.text_area("질문", placeholder="궁금한 것을 입력하세요...", height=120)

if st.button("답변 받기", type="primary"):
    if not st.session_state.api_key:
        st.error("❌ 왼쪽 사이드바에서 API Key를 먼저 입력해주세요.")
    elif not user_question.strip():
        st.warning("⚠️ 질문을 입력해주세요.")
    else:
        with st.spinner("LLM이 답변을 생성 중입니다..."):
            try:
                answer = get_llm_response(st.session_state.api_key, user_question)
                st.subheader("📝 LLM 응답")
                st.write(answer)
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
