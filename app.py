import streamlit as st
import cohere
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
cohere_api_key = os.getenv("COHERE_API_KEY")

# Initialize Cohere
co = cohere.Client(cohere_api_key)

# Title
st.title("💬 JARVIS 2.0")

# Chat history tracking
if "chathistory" not in st.session_state:
    st.session_state.chathistory = []

# Display existing chat history
for msg in st.session_state.chathistory:
    if msg["role"] == "USER":
        with st.chat_message("user"):
            st.markdown(msg["message"])
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["message"])

# Input for new message
userinput = st.chat_input("Type your message...")

# If user sends a message
if userinput:
    st.session_state.chathistory.append({"role": "USER", "message": userinput})
    with st.chat_message("user"):
        st.markdown(userinput)

    try:
        # Call Cohere's chat API
        response = co.chat(
            message=userinput,
            chathistory=st.session_state.chathistory,
            model="command-nightly"
        )
        botreply = response.text.strip()
        st.session_state.chathistory.append({"role": "CHATBOT", "message": botreply})
        with st.chat_message("assistant"):
            st.markdown(botreply)
    except Exception as e:
        st.error(f"Error: {e}")

#Button to show full history
if st.button("📜 Show Full Conversation History"):
    with st.expander("Conversation Log"):
        for msg in st.session_state.chathistory:
            role = "🧑 You" if msg["role"] == "USER" else "🤖 Bot"
            st.markdown(f"**{role}:** {msg['message']}")
