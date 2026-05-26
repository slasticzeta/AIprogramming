import streamlit as st
from openai import OpenAI
import time

# ── 페이지 설정 ──────────────────────────────────────────
st.set_page_config(page_title="ChatPDF", page_icon="📄")
st.title("📄 ChatPDF")
st.caption("PDF 파일을 업로드하면 해당 내용을 기반으로 대화할 수 있습니다.")

# ── session_state 초기화 ─────────────────────────────────
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "pdf_messages" not in st.session_state:
    st.session_state.pdf_messages = []
if "vector_store_id" not in st.session_state:
    st.session_state.vector_store_id = None
if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None

# ── 사이드바 ──────────────────────────────────────────────
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

    # Clear 버튼: vector store 삭제 + 대화 초기화
    if st.button("🗑️ Clear (Vector Store 삭제)", type="secondary", use_container_width=True):
        if st.session_state.vector_store_id and st.session_state.api_key:
            try:
                client = OpenAI(api_key=st.session_state.api_key)
                client.vector_stores.delete(st.session_state.vector_store_id)
            except Exception:
                pass
        st.session_state.vector_store_id = None
        st.session_state.uploaded_file_name = None
        st.session_state.pdf_messages = []
        st.rerun()

    # 현재 업로드된 파일 표시
    if st.session_state.uploaded_file_name:
        st.info(f"📎 현재 파일: {st.session_state.uploaded_file_name}")

# ── PDF 업로드 & Vector Store 생성 ───────────────────────
if not st.session_state.vector_store_id:
    uploaded_file = st.file_uploader("PDF 파일을 업로드하세요 (1개만 가능)", type=["pdf"])

    if uploaded_file and st.session_state.api_key:
        with st.spinner("PDF를 분석하는 중입니다... 잠시만 기다려주세요."):
            try:
                client = OpenAI(api_key=st.session_state.api_key)

                # 1. Vector Store 생성
                vector_store = client.vector_stores.create(
                    name=f"chatpdf_{uploaded_file.name}"
                )

                # 2. PDF 파일 업로드 및 Vector Store에 추가
                file_response = client.vector_stores.files.upload_and_poll(
                    vector_store_id=vector_store.id,
                    file=(uploaded_file.name, uploaded_file.getvalue(), "application/pdf"),
                )

                # 3. 완료 대기
                while True:
                    vs = client.vector_stores.retrieve(vector_store.id)
                    if vs.file_counts.in_progress == 0:
                        break
                    time.sleep(1)

                st.session_state.vector_store_id = vector_store.id
                st.session_state.uploaded_file_name = uploaded_file.name
                st.session_state.pdf_messages = []
                st.success(f"✅ '{uploaded_file.name}' 업로드 완료! 이제 질문하세요.")
                st.rerun()

            except Exception as e:
                st.error(f"파일 업로드 중 오류가 발생했습니다: {e}")

    elif uploaded_file and not st.session_state.api_key:
        st.warning("⚠️ 사이드바에서 API Key를 먼저 입력해주세요.")

else:
    # ── 대화 화면 ─────────────────────────────────────────
    # 기존 대화 출력
    for msg in st.session_state.pdf_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # 사용자 입력
    user_input = st.chat_input("PDF 내용에 대해 질문하세요...")

    if user_input:
        st.session_state.pdf_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            with st.spinner("답변 생성 중..."):
                try:
                    client = OpenAI(api_key=st.session_state.api_key)

                    # OpenAI Responses API + File Search 사용
                    response = client.responses.create(
                        model="gpt-5.4-mini",
                        input=user_input,
                        tools=[{
                            "type": "file_search",
                            "vector_store_ids": [st.session_state.vector_store_id]
                        }],
                    )

                    # 텍스트 응답 추출
                    answer = ""
                    for block in response.output:
                        if hasattr(block, "content"):
                            for content in block.content:
                                if hasattr(content, "text"):
                                    answer += content.text

                    if not answer:
                        answer = "답변을 생성하지 못했습니다. 다시 시도해주세요."

                    st.write(answer)
                    st.session_state.pdf_messages.append({"role": "assistant", "content": answer})

                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")
