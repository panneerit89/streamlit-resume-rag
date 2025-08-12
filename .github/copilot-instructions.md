<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Resume RAG Chatbot Project Instructions

This is a Python project that creates a RAG (Retrieval Augmented Generation) chatbot for processing and querying resume PDFs.

## Project Context
- **Framework**: Streamlit for web interface
- **AI/ML Stack**: LangChain, HuggingFace Transformers, FAISS
- **Document Processing**: PyPDF2/pypdf for PDF handling
- **Main File**: `rag_chatbot.py`

## Code Style Guidelines
- Follow PEP 8 Python style guidelines
- Use descriptive variable names
- Add error handling for file operations and model loading
- Include docstrings for functions
- Use session state for Streamlit components

## Key Components
- PDF document loading and text splitting
- Vector embeddings and FAISS indexing
- HuggingFace pipeline for text generation
- RetrievalQA chain for question answering
- Streamlit UI for file upload and querying

## Dependencies Management
- All dependencies are listed in `requirements.txt`
- Use virtual environment for isolation
- Pin specific versions for reproducibility
