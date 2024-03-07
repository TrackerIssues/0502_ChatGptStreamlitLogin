import streamlit as st

st.set_page_config(
    page_title="ChatGpt Api",
    page_icon="⚡️"
)


sName, bAuthentication_status, sUsername = st.session_state["Auth"].login("main")

if bAuthentication_status :

    st.session_state["Auth"].logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {sName} !")










else :
    # st.error("🚨", "🔥", "🤖")
    # st.error("🚨 Login First!")
    pass