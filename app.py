import streamlit as st
import cohere

# Set black background using custom CSS
st.markdown(
    "<style>body {background-color: #000000; color: white;} .stTextInput, .stTextArea, .stButton > button {background-color: #1c1c1c !important; color: white !important; border: 1px solid #555;} .stTextInput > div > div > input {background-color: #1c1c1c !important; color: white !important;} .stTextArea textarea {background-color: #1c1c1c !important; color: white !important;}</style>",
    unsafe_allow_html=True
)

# Initialize Cohere
co = cohere.Client("tjIaUVtkm9CsXYoSR2mAcn2Dr1oBGQ0OtQNtd0j4")  # Replace with your API key

# UI Title
st.title("💬 Text Reply Chatbot with Cohere")

# Add clear button
if st.button("🧹 Clear Chat"):
    st.session_state.chat_history = []

# Chat history tracking
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Text input
user_input = st.text_input("You:", "")

# When user types something
if user_input:
    st.session_state.chat_history.append({"role": "USER", "message": user_input})

    try:
        response = co.chat(
            message=user_input,
            chat_history=st.session_state.chat_history,
            model="command-nightly"  # Use Chat-compatible model
        )
        bot_reply = response.text.strip()
        st.session_state.chat_history.append({"role": "CHATBOT", "message": bot_reply})
        st.text_area("🤖 Bot:", value=bot_reply, height=100)

    except Exception as e:
        st.error(f"Error: {e}")

# Display full conversation
with st.expander("📜 Conversation History"):
    for msg in st.session_state.chat_history:
        role = "🧑 You" if msg["role"] == "USER" else "🤖 Bot"
        st.markdown(f"**{role}:** {msg['message']}")
