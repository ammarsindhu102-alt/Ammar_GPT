import streamlit as st
from groq import Groq

# 1. Grab the Secure Hidden API Key
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    st.warning("⚠️ Enter your Groq API Key to test locally, or configure Advanced Settings in Streamlit Cloud.")
    GROQ_API_KEY = "your-temporary-local-key-here"

# Initialize Client
client = Groq(api_key=GROQ_API_KEY)

st.title("🧠 High-Intelligence Groq Assistant")

# 2. Perfect Memory Logic + System Prompt
# The system prompt ensures the model utilizes its maximum logical capacity.
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are an elite, high-intelligence AI assistant. "
        "Provide structurally sound, deeply analytical, and highly accurate answers. "
        "Break complex tasks down step-by-step and maintain perfect context."
    )
}

if "messages" not in st.session_state:
    # Visible chat history for the screen
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hello! I am your high-intelligence assistant, optimized for complex reasoning. Ask me anything."}
    ]

# 3. Render Visual Layout Elements
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 4. Streamlined Processing Loop
if user_input := st.chat_input("Ask a complex question..."):
    
    # Store and show user input immediately
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.spinner("Analyzing data..."):
        try:
            # Build the payload injects the system rules at index 0 for maximum intelligence guidance
            api_payload = [SYSTEM_PROMPT] + st.session_state.messages
            
            # Request completion using Groq's premium reasoning model
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",  # Elite tier intelligence model on Groq
                messages=api_payload,
                temperature=0.3,             # Low temperature ensures highly logical and accurate factual reasoning
                max_tokens=4096
            )
            
            reply = response.choices.message.content
            
            # Commit the reply to state history and render
            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.write(reply)
                
        except Exception as e:
            st.error(f"Execution Error: {e}. If the 120B model is rate-limited, switch to 'llama-3.3-70b-versatile'.")
