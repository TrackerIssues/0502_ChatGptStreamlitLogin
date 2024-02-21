import openai
import streamlit as st

openai.api_key = st.secrets["OpenAiApiKey"] 


def RequestChatGpt( 
        sPrompt,
        sRoleSys = "당신은 유능한 한글 카피 도우미",
        sModel = "gpt-3.5-turbo",
        bStream = False,
) :
    lstMessage = [
        { "role" : "system",
         "content" : sRoleSys},
         { "role" : "user",
          "content" : sPrompt}
    ]

    res = openai.ChatCompletion.create(
        model = sModel,
        messages = lstMessage,
        stream = bStream,
    )
    return res

def PrintStreamResponse( response ) :
    sMessage = ""
    oPlaceHolder = st.empty()
    for chunk in response :
        delta = chunk.choices[0]["delta"]
        if "content" in delta :
            sMessage += delta["content"]
            oPlaceHolder.markdown(sMessage + "⇤ ")
        else :
            break
    oPlaceHolder.markdown(sMessage)
    return sMessage
