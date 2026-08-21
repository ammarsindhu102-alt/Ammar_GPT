
import streamlit as st
from openai import OpenAI
# 1. Page Styling
st.set_page_config(page_title="Ammar's_GPT", page_icon="🤖", layout="centered")
# This completely hides the default Streamlit platform headers and menus
hide_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide_style, unsafe_allow_html=True)
st.title("🤖 Ammar's_GPT")
st.caption("The official custom AI assistant created by Ammar.")
# 2. Secure Key Verification
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("Missing API Key. Please add it to your Streamlit settings dashboard.")
    st.stop()
# 3. Persistent Memory & Custom Rules
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": "You are Ammar's_GPT, an elite custom AI assistant created by Ammar. Be helpful, incredibly smart, direct, and keep answers concise."
        }
    ]
# 4. Show Chat History
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
# 5. User Input Loop
if user_prompt := st.chat_input("Ask Ammar's_GPT something..."):
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    # 6. Stream Live Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            for response in client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages,
                stream=True,
            ):
                full_response += (response.choices.delta.content or "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Error: {e}")
            
    st.session_state.messages.append({"role": "assistant", "content": full_response})
