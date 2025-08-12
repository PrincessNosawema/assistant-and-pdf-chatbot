import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    ChatPromptTemplate
)

def generate_ai_response(prompt_chain):
    # Initialize the chat engine with fixed model
    llm_engine = ChatOllama(
        model="gemma3:1b",
        base_url="http://localhost:11434",
        temperature=0.3
    )

    processing_pipeline = prompt_chain | llm_engine | StrOutputParser()
    return processing_pipeline.invoke({})

def build_prompt_chain():
    prompt_sequence = []
    for msg in st.session_state.message_log:
        if msg["role"] == "User":
            prompt_sequence.append(HumanMessagePromptTemplate.from_template(msg["content"]))
        elif msg["role"] == "Assistant":
            prompt_sequence.append(AIMessagePromptTemplate.from_template(msg["content"]))
    return ChatPromptTemplate.from_messages(prompt_sequence)

def ai_response(user_query):
    # Save the user's message in the conversation log
    st.session_state.message_log.append({"role": "User", "content": user_query})
    
    # Display the user's message in the chat UI
    with st.chat_message("User"):
        st.markdown(f'⏳⚙️⌛ Processing your current message:\n\n"{user_query}"')
    
    # Generate AI response based on conversation history
    with st.spinner(f"🧠 Processing...\n⏱️ Wait a little..."):
        response = generate_ai_response(build_prompt_chain())
        
    # Save the AI's reply in the conversation log
    st.session_state.message_log.append({"role": "Assistant", "content": response})
    
    # Rerun to update chat display
    st.rerun()
    
# Clear message log
def clear_log():
    st.session_state.message_log = []