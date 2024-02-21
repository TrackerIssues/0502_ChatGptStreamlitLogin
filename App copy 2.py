import streamlit as st
import pickle
from pathlib import Path 
# from Page1CopyWriter import Page1View
from common import *


import streamlit_authenticator as stauth

st.set_page_config(
    page_title="ChatGpt Api",
    page_icon="🧠"
)


# --- User Authentication ---

names = ["Issues Tracker", "Tracking Issues"]
usernames = ["tracker", "trackingissues"]

sFileName = Path(".").parent / "PassWord.pkl"

with sFileName.open("rb") as file :
    sPassWords = pickle.load(file)

credentials = {
        "usernames":{
            usernames[0]:{
                "name":names[0],
                "password":sPassWords[0]
                },
            usernames[1]:{
                "name":names[1],
                "password":sPassWords[1]
                }            
            }
        }


authenticator = stauth.Authenticate(credentials, "app_home", "auth", cookie_expiry_days=0)

sName, bAuthentication_status, sUsername = authenticator.login("main")


if bAuthentication_status == False :
    st.error("Username / Password is incorrect")


if bAuthentication_status == None :
    st.warning("Please enter your username and password")


bCopyWriter = False

if bAuthentication_status :

    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {sName} !")


    st.title("ChatGpt Api Service")

    # st.subheader("Develoopment various services on yourself.")

    # with st.sidebar :
    #     st.markdown("# AI Copy Writer")
    #     bCopyWriter = st.button("On Copy Writer")

    # if bCopyWriter :
    #     lstTab = ["Copy Writer Tab", "Sub Tab"]
    #     tab1, tab2 = st.tabs(lstTab)

    #     with tab1:
    #         views = Page1View()

    # if bCopyWriter :
        # Page1View()
            

    st.subheader("AI를 이용해서 손쉽게 마케팅 문구를 작성해 보세요!")

    bCheckInput = st.toggle("예시로 채우기")
    dicExample ={
        "sProductName" : "만성질환 예측모형 개발",
        "sProductDesc" : "고혈압 AI 예측모형 개발",
        "lstKeyWord" : ["시계열 추이", "위험요인", "상대위험도", "개인 맞춤"]
    }

    sQuery = "크롤링 소프트웨어 SNS 마케팅을 위한 카피 3개 만들어 줘"
    sRole = "당신은 한글 전문 카피라이터"
    sQueryTemplate = """
    제품 혹은 브랜드를 SNS에 광고하기 위한 문구를 {iNum}개 생성해 주세요.
    자극적이고 창의적으로 작성해 주세요.
    명사 위주로 간결하게 작성해 주세요.
    반드시 {iMaxWord} 단어 이내로 작성해 주세요.
    키워드가 있을 경우, 반드시 키워드 중 하나를 포함해야 함.
    이모지를 적절하게 사용해 주세요.
    ---
    제품명 : {sProductName}
    제품 설명 : {sProductDesc}
    키워드 : {lstKeyWord}
    ---
    """.strip()

    with st.form("form") :
        col1, col2, col3 = st.columns(3)
        with col1 :
            sSubject = st.text_input(
                "주제",
                placeholder=dicExample["sProductName"], 
                value=dicExample["sProductName"] if bCheckInput else "")
        with col2 :
            iMaxWord = st.number_input(
            label="최대 단어 수",
            min_value=5,
            max_value=20,
            step=1,
            value=10
        )
        with col3 :
            iScript = st.number_input(
            label="생성할 문구 수",
            min_value=1,
            max_value=20,
            step=1,
            value=5
        )
        
        sDescript = st.text_input(
            "한줄 설명",
            placeholder=dicExample["sProductDesc"],
            value=dicExample["sProductDesc"] if bCheckInput else ""
            )

        st.text("포함할 키워드를 입력해 주세요!")
        col1, col2, col3 = st.columns(3) 
        with col1:
            sKeyWord1 = st.text_input(
                label="Keyword 1",
                placeholder="키워드 1",
                value=dicExample["lstKeyWord"][0] if bCheckInput else ""
            )
        with col2:
            sKeyWord2 = st.text_input(
                label="Keyword 2",
                placeholder="키워드 2",
                value=dicExample["lstKeyWord"][1] if bCheckInput else ""
            )
        with col3:
            sKeyWord3 = st.text_input(
                label="Keyword 3",
                placeholder="키워드 3",
                value=dicExample["lstKeyWord"][2] if bCheckInput else ""
            )

        bSubmit = st.form_submit_button("Submit")


    if bSubmit :
        if not sSubject :
            st.error("주제를 작성해 주세요!")
        elif not sDescript :
            st.error("설명을 추가 해 주세요!")
        else :
            lstKeyWord = [sKeyWord1, sKeyWord2, sKeyWord3]
            lstKeyWord = [ x for x in lstKeyWord if x]

            sQuery = sQueryTemplate.format(
                        iNum = iScript,
                        iMaxWord = iMaxWord,
                        sProductName = sSubject,
                        sProductDesc = sDescript,
                        lstKeyWord = lstKeyWord
                    )
            
            with st.spinner("카피를 생성 중 입니다!") :    
                res = RequestChatGpt(
                    sPrompt= sQuery,
                    sRoleSys= sRole,
                    bStream=True
                )

            PrintStreamResponse(res)



            st.success("카피를 작성합니다!")

            