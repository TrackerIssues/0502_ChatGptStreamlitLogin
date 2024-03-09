import streamlit as st
from common import *


st.set_page_config(
    page_title="ChatGpt Api",
    page_icon="👨🏻‍🍳"
)

sName, bAuthentication_status, sUsername = st.session_state["Auth"].login("main")

if bAuthentication_status :

    st.session_state["Auth"].logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {sName} !")


    st.title("🎯 ChatGpt Resume Helper Service")
    st.subheader("지원 기업과 지원자의 경험을 바탕으로 초안을 만들어 줍니다.")

    # bAutoComplete = st.toggle("에제로 채우기")
    col1, col2, col3 = st.columns(3)
    with col1 :
        bAutoComplete = st.toggle("예시로 채우기")
    with col2 :
        pass
    with col3 :
        bEng = st.toggle("영어로 작성")

    dcExample = {
    "company" : "카카오 헬스케어",
    "position" : "디지털헬스케어 수석연구원",
    "maxlength" : 300,
    "question" : "소속 조직의 공동과업 달성하는 과정에서 발생했던 어려움과 그 어려움을 극복하기 위해 기울인 노력에 대해 구체적인 사례를 바탕으로 기술해 주세요",
    "experience" : "보건연구소 역학파트장 및 디지털헬스케어파트장 역임\n 연구과제 책임연구원 의사부장의 퇴사를 대신하여 사내 최초 만성질환 통계모형 개발 및 시계열 변화융을 반영한 AI 신개념 예방서비스 개발 "
    }
    
    TemplePrompt = """
    기업 입사용 자기소개서를 작성해야 합니다.
    답변해야 하는 질문과 이에 관련된 경험을을 참고해서 자기소개서를 작성해 주세요.
    반드시 {nMaxLength} 단어 이내로 작성해야 합니다.
    단락마다 소제목을 넣어주세요

    ---
    지원 회사 : {sCompany}
    지원 직무 : {sPosition}
    질문 : {sQuestion}
    관련 경험 : {sExperience}
    ---
    """.strip()


    with st.form("form") :
        col1, col2, col3 = st.columns(3)
        with col1 :
            company = st.text_input(
                "지원 기업",
                value=dcExample["company"] if bAutoComplete else "",
                placeholder=dcExample["company"]
                )
        with col2 :
            position = st.text_input(
                "지원 직무",
                value=dcExample["position"] if bAutoComplete else "",
                placeholder=dcExample["position"]
                )
        with col3 :
            maxLenght = st.number_input(
            "최대 단어 수",
            min_value=150,
            max_value=3000,
            step=50,
            value=300
        )
        
        question = st.text_area(
            "필수 작성 내용",
            value=dcExample["question"] if bAutoComplete else "",
            placeholder=dcExample["question"]
            )
        experience = st.text_area(
            "관련 경험 또는 경력",
            value=dcExample["experience"] if bAutoComplete else "",
            placeholder=dcExample["experience"]
            )

        bSubmit = st.form_submit_button("제출하기")

    if bSubmit :
        if not company :
            st.error("지원하는 회사를 입력해 주세요!")
        elif not position :
            st.error("지원하는 직무를 입력해 주세요!")
        elif not question :
            st.error("필수 내용을 입력해 주세요!")
        elif not experience :
            st.error("지원자의 경험을 입력해 주세요!")
        else : 

            sQuery = TemplePrompt.format(
                        sCompany    = company,
                        sPosition   = position,
                        sQuestion   = question,
                        sExperience = experience,
                        nMaxLength  = maxLenght //3 , 
                    )
            # st.markdown(prompt)


            sRole = "당신은 취업 전문 컨설턴트 또는 전문직 헤더 헌터입니다."
            if bEng :
                sRole = "당신은 미국인 전문 consultant 반드시 영어로만 작성해야 합니다"
                sQuery = "다음 내용을 반드시 영어로 작성해야 합니다\n" + sQuery
            

            with st.spinner("카피를 생성 중 입니다!") :    
                res = RequestChatGpt(
                    sPrompt= sQuery,
                    sRoleSys= sRole,
                    bStream=True
                )

            msg = PrintStreamResponse(res)

            st.markdown( f"**공백 포함 단어 수 : {len(msg)}**")

            st.success("초안을 작성했습니다!")
            # st.success( "제출!" )






else :
    # st.markdown('<a href="ReadMe" target=_top>Login First</a>', unsafe_allow_html=True)
    pass