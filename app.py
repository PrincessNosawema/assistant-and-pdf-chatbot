import html
import streamlit as st
from chat_ai.main_ai import ai_response, clear_log
from chat_pdf.main_pdf import clear_chat, pdf_processor, respond_to_pdf

def main():
    # Page configuration
    st.set_page_config(page_title="AI Assistant & PDF Chatbot", page_icon="🤖📚", layout="wide")
    
    # Main content
    tab1, tab2 = st.tabs(["🤖 AI Assistant", "📚 PDF Chatbot"])

    with tab1:
        st.title("🤖 AI Assistant built with Gemma 3 1B")
        st.caption("🧠 Your intelligent conversation partner") 
        
        # Session state management
        if "message_log" not in st.session_state:
            st.session_state.message_log = [{"role": "Assistant", "content": "Hi! I'm here to help. What would you like to discuss? 💬"}]

        # Display all previous messages
        for message in st.session_state.message_log:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input for processing
        user_query = st.chat_input("Ask me anything... 🙂")
        
        # Processing
        if user_query:
            try:
                ai_response(user_query)
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")
                
        # Clear conversation button
        st.write("---")
        st.button("Clear Entire Conversation", on_click=lambda: clear_log())
        
    with tab2:
        st.title("📚 Advanced PDF Chatbot built with Gemma 3 1B")
        st.caption("🎓 Unlock your document — one smart chat at a time")
        
        # Session state management
        if "chat_history" not in st.session_state:
            clear_chat()
        if "vector_db" not in st.session_state:
            st.session_state.vector_db = None
        if "document_text" not in st.session_state:
            st.session_state.document_text = ""
        if "chunks" not in st.session_state:
            st.session_state.chunks = []
            
        # PDF upload section
        uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
        
        if uploaded_file:
            with st.spinner("Processing PDF..."):
                # Clear previous data
                st.session_state.document_text = ""
                st.session_state.chunks = []
                st.session_state.vector_db = None
                
                try:
                    # Process PDF
                    pdf_processor(uploaded_file)
                    
                    # Generate the chat interface if the uploaded PDF is processed successfully
                    st.header("Chat with Document")
                    user_input = st.text_input("Ask a question about the PDF 📑", key="user_input")
                    
                except Exception as e:
                    st.error(f"Error processing PDF: {str(e)}")
                
        if st.button("Send"):
            if not uploaded_file:
                st.warning("Please upload a PDF first")
            elif not user_input:
                st.warning("Please enter a question")
            else:
                with st.spinner("Searching document..."):
                    # Generate prompt and response
                    try:
                        response, cited_pages = respond_to_pdf(user_input)
                        
                        # Add to chat history with citation
                        st.session_state.chat_history.append({
                            "question": user_input,
                            "answer": response,
                            "references": sorted(cited_pages)
                        })
                        
                    except Exception as e:
                        st.error(f"Error generating response: {str(e)}")
        
        # Display chat history
        st.header("Conversation History")
        for chat in reversed(st.session_state.chat_history):
            # User message
            st.markdown(
                f"""
                <div style='background-color:#2f2f2f; color:white; padding:10px; border-radius:10px; margin-bottom:5px;'>
                    <div style='font-weight:bold; font-size:1.5em; margin-bottom:5px;'>USER:</div>
                    {html.escape(chat['question'])}
                </div>
                """,
                unsafe_allow_html=True
            )
        
            # AI message
            st.markdown(
                f"""
                <div style='background-color:#1a1a1a; color:white; padding:10px; border-radius:10px; margin-bottom:5px;'>
                    <div style='font-weight:bold; font-size:1.5em; margin-bottom:5px;'>AI:</div>
                    {html.escape(chat['answer'])}
                </div>
                """,
                unsafe_allow_html=True
            )
        
            # References
            references = chat['references']
            page_text = "Pages" if len(references) > 1 else "Page"
            st.caption(f"References: {page_text} {', '.join(map(str, references))}")
            st.write("---")
            
        # Reset button
        st.button("Clear Conversation", on_click=lambda: clear_chat())

if __name__ == "__main__":
    main()