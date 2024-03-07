import streamlit as st


st.set_page_config(
    page_title="ChatGpt Api",
    page_icon="👨🏻‍🍳"
)

sName, bAuthentication_status, sUsername = st.session_state["Auth"].login("main")

if bAuthentication_status :

    st.session_state["Auth"].logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {sName} !")


    st.title("ChatGpt Api Resume Helper Service")





else :
    # st.markdown('<a href="ReadMe" target=_top>Login First</a>', unsafe_allow_html=True)
    pass