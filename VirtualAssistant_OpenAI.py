import streamlit as st
import openai
import pyttsx3
import sounddevice as sd
import numpy as np
import wave
import os

# Set up OpenAI API Key
openai.api_key = "your_openai_api_key"

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

# Store conversation history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "system", "content": "You are a helpful AI assistant."}]

def chat_with_gpt(user_input):
    """Sends conversation history to OpenAI GPT API and returns the response."""
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=st.session_state.chat_history
    )

    assistant_reply = response["choices"][0]["message"]["content"]
    
    # Append assistant's reply to history
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_reply})

    return assistant_reply

def speech_to_text():
    """Uses OpenAI Whisper API to convert recorded speech to text."""
    audio_file = "speech_input.wav"
    samplerate = 16000
    duration = 5  # Max recording time in seconds

    st.write("🎙️ Recording... Speak now")
    recording = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()

    # Save recorded audio
    with wave.open(audio_file, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(recording.tobytes())

    st.write("🔍 Transcribing speech...")
    with open(audio_file, "rb") as f:
        transcript = openai.Audio.transcribe("whisper-1", f)

    os.remove(audio_file)  # Delete the file after processing
    return transcript["text"]

def speak(text):
    """Converts text to speech."""
    engine.say(text)
    engine.runAndWait()

# Streamlit UI
st.title("🤖 AI Virtual Assistant")
st.write("Type your message or use voice input to chat.")

# Chat history display
st.subheader("📝 Chat History")
for message in st.session_state.chat_history:
    role = "👤 You" if message["role"] == "user" else "🤖 Assistant"
    st.markdown(f"**{role}:** {message['content']}")

# Input options
col1, col2 = st.columns(2)

with col1:
    user_input = st.text_input("💬 Type your message", "")

with col2:
    if st.button("🎤 Use Voice Input"):
        user_input = speech_to_text()
        st.write(f"🎙️ You said: {user_input}")

if user_input:
    response = chat_with_gpt(user_input)
    st.markdown(f"**🤖 Assistant:** {response}")
    speak(response)
