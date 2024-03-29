#coding:utf-8

import streamlit as st
import google.generativeai as genai
from markdown import Markdown
from io import StringIO
from datetime import datetime
import subprocess

def unmark_element(element, stream=None):
    if stream is None:
        stream = StringIO()
    if element.text:
        stream.write(element.text)
    for sub in element:
        unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()


# patching Markdown
Markdown.output_formats["plain"] = unmark_element
__md = Markdown(output_format="plain")
__md.stripTopLevelTags = False


def unmark(text):
    return __md.convert(text)

with st.sidebar:
    st.markdown(
        """
       <style>
       [data-testid="stSidebar"][aria-expanded="true"]{
           min-width: 330px;
           max-width: 330px;
       }
       """,
        unsafe_allow_html=True,
    )
    st.title("Welcome back!")
    GOOGLE_API_KEY = st.text_input("API Key", key="api_key", type="password")
    st.markdown("[Get a Gemini API key](https://aistudio.google.com/app/apikey)")
    genai.configure(api_key=GOOGLE_API_KEY)
        # Initialize Gemini-Pro 
    model = genai.GenerativeModel('gemini-pro')
    st.markdown("\n\n\n\n\n\n\n\n\n Made by lengoc-quang")


# Gemini uses 'model' for assistant; Streamlit uses 'assistant'
def role_to_streamlit(role):
  if role == "model":
    return "assistant"
  else:
    return role

# Add a Gemini Chat history object to Streamlit session state
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history = [])

# Display Form Title
st.title("Welcome to AI Chatbot!")
st.markdown("###### Based in Gemini Pro API")

# Display chat messages from history above current input box
for message in st.session_state.chat.history:
    with st.chat_message(role_to_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Accept user's next message, add to context, resubmit context to Gemini
if prompt := st.chat_input("Enter question here..."):
    if GOOGLE_API_KEY == '':
        st.error("You must enter an API key!")
    else:
        ms = [prompt]
        # Display user's last message
        st.chat_message("user").markdown(prompt)
        f=open('history.log', "a", encoding='utf-8')
        f.write("You: " + unmark(prompt) +"\n\n")
        f.close()
    
        # Send user entry to Gemini and read the response
        response = st.session_state.chat.send_message(prompt) 
        
        # Display last 
        with st.chat_message("assistant"):
            st.markdown(response.text)
            f=open('history.log', "a", encoding='utf-8')
            f.write("Chatbot: "+unmark(response.text) + "\n\n")
            f.close()
