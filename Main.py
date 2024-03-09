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


# authenticator = stauth.Authenticate(credentials, "app_home", "auth", cookie_expiry_days=30)
st.session_state["Auth"] = stauth.Authenticate(credentials, "app_home", "auth", cookie_expiry_days=1)

# sName, bAuthentication_status, sUsername = authenticator.login("main")
sName, bAuthentication_status, sUsername = st.session_state["Auth"].login("main")



if bAuthentication_status == False :
    st.error("Username / Password is incorrect")


if bAuthentication_status == None :
    st.warning("Please enter your username and password")


if "StateLogin" not in st.session_state :
    st.session_state["bLogin"] = False



if bAuthentication_status :

    st.session_state["bLogin"] = True
    st.session_state["sName"] = sName

    st.session_state["Auth"].logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {sName} !")

    




    st.title("ChatGpt Api Service")

    st.subheader("Develoopment various services on yourself.")

            