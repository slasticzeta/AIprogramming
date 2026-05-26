import streamlit as st
from openai import OpenAI

# ── 페이지 설정 ──────────────────────────────────────────
st.set_page_config(page_title="부경대 도서관 챗봇", page_icon="📚")
st.title("📚 국립부경대학교 도서관 챗봇")
st.caption("도서관 규정을 기반으로 답변합니다.")

# ── 도서관 규정 문자열 ─────────────────────────────────────
LIBRARY_RULES = """
국립부경대학교 도서관 규정
[시행 2023.12.27] [부경대학교학교규정 제1316호, 2023.12.27, 타법개정]

제1장 총칙
제1조(목적) 이 규정은 「대학도서관진흥법」과 「국립부경대학교 학칙」 제11조의3에 따라 국립부경대학교 도서관의 발전계획 수립과 진행, 직원의 배치, 학술정보자료의 확보와 효율적인 이용 및 관리에 관한 사항을 규정함을 목적으로 한다.
제2조(임무) 도서관은 대학교육의 목적달성을 위하여 국내외 각종 정보자료를 수집, 정리, 보존하여 교직원, 학생 및 지역주민들의 연구, 학습에 제공함을 임무로 한다.

제2장 조직
제3조(조직) ① 도서관장의 임기는 2년으로 하되 연임할 수 있다.
② 관장은 도서관 운영에 관한 모든 업무를 총괄한다.
제4조(도서관 운영위원회) 도서관에서는 도서관 운영위원회를 두며, 위원회의 구성과 운영에 관한 사항은 따로 정한다.

제3장 도서관 발전계획
제5조(발전계획의 수립) ① 관장은 5년마다 발전계획 개시 연도의 2월 말일까지 발전계획을 수립한다.
② 관장은 매년 2월말까지 연도별 시행계획을 수립한다.

제4장 직원의 배치 및 교육
제6조(직원의 배치) 총장은 도서관에 법령에서 정한 기준 이상의 사서를 두어야 한다.
제7조(교육 훈련) 도서관에 근무하는 사서 및 전문 직원은 연간 최소 교육시간 이상의 교육·훈련을 이수하여야 한다.

제5장 자료의 수집 및 관리
제8조(자료 구입 예산 및 소장) 기본도서는 학생 1인당 70권 이상, 연간 증가 도서 수는 학생 1인당 2권 이상을 확보하도록 노력하여야 한다.
제9조(자료의 구분) 자료는 단행본, 연속간행물, 참고자료, 전자자료, 비도서자료, 학위논문, 귀중자료, 기타자료로 구분한다.
제13조(자료의 납본) 교내에서 발간되는 자료는 발행일로부터 30일 이내에 2부를 도서관에 납본하여야 한다.

제6장 시설 및 자료의 이용
제17조(시설에 관한 기준) 재학생 1인당 1.2제곱미터 이상의 연면적 시설을 확보하여야 한다.
제18조(자격) 교직원 및 재학생, 관장의 허가를 받은 그 밖의 사람은 도서관 자료 및 시설을 이용할 수 있다.
제19조(개관 시간) 도서관의 개관 시간은 관장이 별도로 정한다.
제20조(휴관일) 도서관의 휴관일은 다음과 같다. 다만, 관장은 필요에 따라 이를 조정할 수 있다.
- 자료실: 공휴일, 개교기념일
- 일반열람실: 설날, 추석
제21조(자료대출) 제18조에 규정된 사람은 본인의 신분증으로 대출할 수 있다.
제22조(대출책수 및 기간) 단행본 대출 책 수 및 기간:
- 전임교원, 겸임교원, 명예교수, 강사: 50책 이내 90일
- 직원, 조교, 대학원생: 20책 이내 30일
- 학부생: 10책 이내 14일
- 전자책 대출: 모든 이용자 5책 이내 5일
제23조(대출 제한 자료) 연속간행물, 참고자료, 학위논문, 귀중자료, 비도서자료는 대출할 수 없다.
제24조(대출기간 중 반납) 휴직, 퇴직, 졸업 등의 사유 발생 시 대출 자료를 즉시 반납하여야 한다. 졸업·수료 예정자는 학위수여일 30일 전부터 대출이 중지된다.
제25조(관내수칙) 자료 또는 물품의 훼손 및 무단 반출, 신분증 대여 및 무단 사용, 지정된 장소 외에서 식음이나 흡연 등을 금지한다.

제9장 제재
제32조(자료대출 중지) 대출한 자료를 기한 내에 반납하지 아니하면 다른 자료 대출 및 도서관 이용을 중지한다.
제33조(자료의 변상) 자료를 분실 또는 훼손하였을 경우 신고일로부터 10일 이내에 동일자료로 변상하여야 한다.
제34조(자료반납 불이행자에 대한 조치) 각종 증명서 발급 보류, 장학금 지급 및 휴학 등 승인 보류 조치를 요청할 수 있다.
제35조(질서 위반자에 대한 조치) 도서관 규정을 위반한 사람에게 도서관 이용 중지 등의 제재를 취할 수 있다.
"""

# ── session_state 초기화 ─────────────────────────────────
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "lib_messages" not in st.session_state:
    st.session_state.lib_messages = []

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
    st.markdown("**💡 질문 예시**")
    st.markdown("- 도서관 휴관일이 언제인가요?")
    st.markdown("- 학부생은 책을 몇 권 빌릴 수 있나요?")
    st.markdown("- 대출 연체하면 어떻게 되나요?")
    st.divider()

    if st.button("🗑️ 대화 초기화", type="secondary", use_container_width=True):
        st.session_state.lib_messages = []
        st.rerun()

# ── 대화 내역 출력 ────────────────────────────────────────
for msg in st.session_state.lib_messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ── 사용자 입력 ───────────────────────────────────────────
user_input = st.chat_input("도서관에 대해 궁금한 것을 물어보세요...")

if user_input:
    if not st.session_state.api_key:
        st.error("❌ 왼쪽 사이드바에서 API Key를 먼저 입력해주세요.")
    else:
        # 사용자 메시지 저장 & 출력
        st.session_state.lib_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # LLM 응답 생성
        with st.chat_message("assistant"):
            with st.spinner("답변 생성 중..."):
                try:
                    client = OpenAI(api_key=st.session_state.api_key)

                    system_prompt = f"""당신은 국립부경대학교 도서관 안내 챗봇입니다.
아래의 도서관 규정을 바탕으로만 답변하세요.
규정에 없는 내용은 "해당 내용은 규정에 명시되어 있지 않습니다. 도서관(051-629-6702)으로 문의해주세요."라고 답변하세요.
항상 한국어로 친절하게 답변하세요.

[도서관 규정]
{LIBRARY_RULES}
"""
                    response = client.chat.completions.create(
                        model="gpt-5.4-mini",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            *st.session_state.lib_messages,
                        ],
                    )
                    answer = response.choices[0].message.content
                    st.write(answer)
                    st.session_state.lib_messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")
