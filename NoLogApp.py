import streamlit as st

st.set_page_config(
    page_title="ChatGpt Api",
    page_icon="🧠"
)

st.title("ChatGpt Api Service")

st.subheader("Develoopment various services on yourself.")

if "StateLogin" not in st.session_state :
    st.session_state["StateLogin"] = ""

