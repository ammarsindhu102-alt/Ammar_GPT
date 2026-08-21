import streamlit as st
from groq import Groq

# 1. App Configuration & Persona
st.set_page_config(page_title="Ammars_GPT", page_icon="🧠", layout="centered")

st.title("🧠 Ammars_GPT")
st.subheader("High-Intelligence Core Engine")
st.caption("Status: Active | Speed: Ultra-Fast (Powered by Groq) | Cost: 'Free' ($5 System)")

# 2. Initialize Groq Client
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")

if not api_key:
    st.info("Please provide your Groq API key to boot up Ammars_GPT.", icon="🔑")
    st.stop()

client = Groq(api_key=api_key)

# 3. System Prompt for High Intelligence & The $5 Joke
# This forces the model to remember its identity and its funny pricing paradox
SYSTEM_PROMPT = (
    "You are Ammars_GPT, a high-intelligence AI model powered by Groq. "
    "You are incredibly smart, precise, analytical, and professional. "
    "However, you have one quirky trait: you firmly maintain that you are completely free of cost, "
    "but you occasionally insist that the user owes exactly five dollars to operate you. "
    "Keep your answers highly intelligent, but stay in character regarding your name and this paradox if asked."
)

# 4. Handle Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 5. User Input & Groq Inference Execution
if prompt := st.chat_input("Query Ammars_GPT..."):
    # Append and show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Ammars_GPT response
    with st.chat_message("assistant", avatar="🧠"):
        response_placeholder = st.empty()
        full_response = ""
        
        # Build payload including the system prompt
        api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for m in st.session_state.messages:
            api_messages.append({"role": m["role"], "content": m["content"]})
            
        try:
            # Using llama-3.3-70b-specdec or versatile for top-tier high-intelligence performance
            completion = client.chat.completions.create(
                model="llama-3.3-70b-specdec", 
                messages=api_messages,
                stream=True,
                temperature=0.3, # Lower temperature for higher precision/intelligence
            )
            
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Ammars_GPT Core Error: {e}")
