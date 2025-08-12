# Resume RAG Chatbot

A Streamlit-based RAG (Retrieval Augmented Generation) chatbot for processing and querying resume PDFs using intelligent pattern matching and vector search.

## Features

- Upload multiple PDF resumes
- Process and index resume content using ChromaDB vector store
- Query candidates using natural language with precise answers
- Pattern-based extraction for specific information (phone, email, skills)
- Fast loading with optimized search algorithms

## Installation

1. Make sure you have Python 3.8+ installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit application:
   ```bash
   streamlit run rag_chatbot.py
   ```

2. Upload PDF resumes using the file uploader
3. Ask specific questions about candidates for precise answers

## Key Improvements

- **Accurate Responses**: Pattern-based extraction eliminates hallucinations
- **Precise Answers**: Direct information extraction without AI generation
- **Fast Performance**: No heavy LLM models, instant responses
- **Reliable Results**: Regex patterns for contact info, skills, and experience

## Dependencies

- Streamlit - Web application framework
- LangChain - Framework for document processing
- ChromaDB - Vector similarity search and storage
- HuggingFace - Embeddings for semantic search
- PyPDF2/pypdf - PDF processing

## Architecture

The application uses:
- **Document Loading**: PyPDFLoader for PDF processing
- **Text Splitting**: RecursiveCharacterTextSplitter for chunking
- **Embeddings**: HuggingFace sentence-transformers/all-MiniLM-L6-v2
- **Vector Store**: ChromaDB for similarity search and persistence
- **Information Extraction**: Pattern-based regex matching for precise answers
- **Search Strategy**: Semantic similarity + pattern recognition

## Supported Query Types

- **Contact Information**: Phone numbers, email addresses
- **Skills & Technologies**: Programming languages, frameworks
- **Experience**: Years of experience, work history
- **General Information**: Education, certifications, projects
