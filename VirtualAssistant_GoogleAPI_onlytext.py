from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

client = genai.configure(api_key= os.getenv("GOOGLE_API_KEY"))

# Assuming there is a method to generate text
def generate_text(prompt):
    response_txt = client.generate(model='gemini-pro', prompt=prompt)
    return response_txt

st.set_page_config(page_title="Q&A Demo", page_icon=":shark")
st.header("LLM Application")
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Input:", key="input")
submit = st.button("Ask the question")

if submit and input:
    response = generate_text(input)
    st.session_state['chat_history'].append(("You", input))
    st.subheader("Gemini Response")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))
st.subheader("Chat History is")

for role, text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")




