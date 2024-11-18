import streamlit as st
from langchain_ollama import OllamaLLM


api_key = os.getenv("LA-daf3bb9222d240b68975010fbbf79d9f528164036d574719a210f7ebd0cf0928")
model = OllamaLLM(model="llama3.2", api_key=api_key)

if "conversation_context" not in st.session_state:
    st.session_state.conversation_context = [
        { "role" : "assistant" , "content" : "Hello! You can ask any health-realted question to me ? (Disclaimer : Only universal facts and data that are considered correct are given. No medical related advice or prescription is given.)"}
    ]

st.title("Sleep Improvement Chatbot")

user_input = st.text_input("Ask your question about sleep:", "")

if st.button("Send"):
    if user_input.strip():

        st.session_state.conversation_context.append({"role": "user", "content": user_input})
        
        try:
            result = model.invoke(input=st.session_state.conversation_context)
            
            st.session_state.conversation_context.append({"role": "assistant", "content": result})
            
            st.write(f"**Assistant:** {result}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a question before clicking 'Send'.")

st.write("## Conversations")
for message in st.session_state.conversation_context:
    role = "You" if message["role"] == "user" else "Assistant"
    st.write(f"**{role}:** {message['content']}")
