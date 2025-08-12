import streamlit as st
import fitz  # PyMuPDF
import ollama
from PIL import Image
import pytesseract
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
import faiss
import io

# PDF processing function
def process_pdf(file):
    doc = fitz.open(stream=file, filetype="pdf")
    text = []
    for page_num, page in enumerate(doc):
        page_text = page.get_text()
        if not page_text.strip():  # If no text, try OCR
            try:
                img = page.get_pixmap()
                img_bytes = img.tobytes()
                page_text = pytesseract.image_to_string(Image.open(io.BytesIO(img_bytes)))
            except Exception as e:
                st.warning(f"OCR failed for page {page_num+1}: {str(e)}")
        text.append((page_num+1, page_text))
    return text

# Text chunking and vector database
def build_vector_database(text_chunks):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode([chunk[1] for chunk in text_chunks])
    
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    
    return index, model

# Search function
def find_relevant_chunks(query, k=3):
    if st.session_state.vector_db is None or not hasattr(st.session_state, "embedding_model"):
        return []
        
    query_embedding = st.session_state.embedding_model.encode([query])
    distances, indices = st.session_state.vector_db.search(query_embedding, k)
    
    relevant_chunks = []
    for idx in indices[0]:
        relevant_chunks.append(st.session_state.chunks[idx])
    return relevant_chunks

# PDF processor
def pdf_processor(uploaded_file):
    processed_text = process_pdf(uploaded_file.getvalue())
    
    # Create text chunks with page numbers
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    
    for page_num, page_text in processed_text:
        chunks = text_splitter.create_documents([page_text])
        for chunk in chunks:
            st.session_state.chunks.append((page_num, chunk.page_content))
    
    # Build vector database
    if st.session_state.chunks:
        st.session_state.vector_db, st.session_state.embedding_model = build_vector_database(st.session_state.chunks)
        st.success(f"PDF processed successfully! {len(st.session_state.chunks)} chunks created")
    else:
        st.warning("No text could be extracted from the PDF")
        
def respond_to_pdf(user_input):
    # Create context with citations
    context = ""
    cited_pages = set()
    for page_num, chunk_text in find_relevant_chunks(user_input):
        context += f"[Page {page_num}]: {chunk_text}\n"
        cited_pages.add(page_num)
        
    # Generate prompt
    prompt = f"""
    Document Context:
    {context}
    
    Question: {user_input}
    
    Answer: Please provide a concise answer based on the document context.
    Include references to pages in parentheses, e.g. (Page 3).
    """
            
    # Generate response
    response = ollama.generate(
        model="gemma3:1b",
        prompt=prompt,
        options={"temperature": 0.7, "max_tokens": 500}
    )
    
    return response["response"], cited_pages
    
# Clear chat history
def clear_chat():
    st.session_state.chat_history = []