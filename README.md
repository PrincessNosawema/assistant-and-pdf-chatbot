# 🤖📚 AI Assistant & PDF Chatbot

An interactive **AI-powered assistant** and **PDF chatbot** built with [Streamlit](https://streamlit.io/), [LangChain](https://www.langchain.com/), [Ollama](https://ollama.com/), and the **Gemma 3 1B** model.

This application lets you:
- **Chat naturally with an AI assistant**
- **Upload PDFs and ask context-aware questions**
- Get **page-referenced answers** for better document navigation
- Run everything locally for **privacy** and **speed**

---

## 🚀 Features

### 🤖 AI Assistant
- Context-aware conversations powered by **Gemma 3 1B**
- Maintains conversation history within your session
- Quick “Clear Conversation” option

### 📚 PDF Chatbot
- Upload PDFs and interact via natural language
- Extracts text with OCR fallback (via Tesseract) for scanned PDFs
- Splits text into intelligent chunks for semantic search
- Uses **FAISS** vector store + sentence embeddings for document retrieval
- Returns answers with **page references** for quick verification

### 🛠 Technical Highlights
- **LangChain Ollama** integration for local LLM inference
- **Sentence Transformers** for semantic similarity search
- **PyMuPDF** for fast PDF parsing
- **Tesseract OCR** for image-based PDF content
- **FAISS** for vector search
- **Streamlit** for rich, interactive UI

---

## 🧩 How It Works

1. **AI Assistant Tab**

   * Collects conversation history from session state
   * Builds a **LangChain ChatPromptTemplate**
   * Sends it to **Gemma 3 1B** via Ollama
   * Displays responses inline

2. **PDF Chatbot Tab**

   * Processes uploaded PDF with PyMuPDF
   * Runs OCR via Tesseract for image-only pages
   * Splits text into chunks and stores them in FAISS
   * Retrieves the most relevant chunks for your query
   * Constructs a contextual prompt for Gemma
   * Returns a cited answer with page numbers

---

## 📂 Project Structure

```plaintext
root/
│
├── app.py                  # Main Streamlit app entry point
├── requirements.txt        # Python dependencies
│
├── chat_ai/
│   └── main_ai.py          # AI Assistant logic
│
└── chat_pdf/
    └── main_pdf.py         # PDF chatbot logic
```

---

## 💻 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/PrincessNosawema/assistant-and-pdf-chatbot
cd assistant-and-pdf-chatbot
```

### 2️⃣ Create and Activate a Virtual Environment

```bash
# Create venv (Python 3.9+ recommended)
python3 -m venv chatenv

# Activate venv
# Mac/Linux:
source chatenv/bin/activate
# Windows:
chatenv\Scripts\activate
```

### 3️⃣ Upgrade pip

```bash
pip install --upgrade pip
```

### 4️⃣ Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Install System Dependencies

#### Tesseract OCR (for scanned PDFs)

```bash
sudo apt-get update
sudo apt-get install -y tesseract-ocr libtesseract-dev
```

#### Ollama (for running Gemma 3 1B locally)

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

---

## ▶️ Running the Application

### 1️⃣ Start Ollama Service

```bash
ollama serve &
```

### 2️⃣ Pull the Gemma 3 1B Model

```bash
ollama pull gemma3:1b
```

### 3️⃣ Launch the Streamlit App

```bash
streamlit run app.py
```

Then, open the provided local URL in your browser (usually `http://localhost:8501`).

---

## 📝 Requirements

### Python Dependencies

See [`requirements.txt`](requirements.txt):

* `streamlit>=1.28.0`
* `langchain-ollama>=0.1.0`
* `langchain-core>=0.2.0`
* `langchain>=0.2.0`
* `sentence-transformers>=2.2.2`
* `faiss-cpu>=1.7.4`
* `PyMuPDF>=1.23.0`
* `pytesseract>=0.3.10`
* `Pillow>=10.0.0`
* `pdf2image>=1.17.0`
* `numpy>=1.24.0`
* `ollama>=0.1.8`

---

## ⚠️ Notes & Best Practices

* **Model Availability:** Ensure `gemma3:1b` is downloaded in Ollama before running.
* **Tesseract OCR:** Required only for PDFs without embedded text.
* **Performance:** Local LLM inference speed depends on your hardware.
* **Persistence:** Session data is stored in Streamlit session state; restarting the app clears it.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).