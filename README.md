# 🤖 Resume RAG Chatbot (PWA)

A Progressive Web App (PWA) built with Streamlit for AI-powered resume analysis and candidate screening. Features a ChatGPT-5 inspired interface with offline capabilities.

## ✨ Features

### 🎯 Core Functionality
- **📤 Upload multiple PDF resumes** with drag & drop interface
- **🔍 AI-powered search** using ChromaDB vector store
- **💬 Natural language queries** with precise pattern-matching answers
- **📱 Progressive Web App** - installable on mobile and desktop
- **🌐 Offline support** with service worker caching

### 🎨 Modern Interface
- **ChatGPT-5 inspired design** with dark theme
- **Glassmorphism effects** and smooth animations
- **Responsive layout** optimized for all devices
- **Fast loading** with optimized search algorithms

### 🔍 Smart Search Capabilities
- Extract contact information (phone, email)
- Identify technical skills and programming languages
- Find experience levels and years of work
- Compare candidates across multiple criteria

## 🚀 Quick Start

### Local Development
```bash
# Clone the repository
git clone https://github.com/panneerit89/streamlit-resume-rag.git
cd streamlit-resume-rag

# Install dependencies
pip install -r requirements-python.txt

# Run the application
streamlit run rag_chatbot.py
```

### 🌐 Netlify Deployment

#### Option 1: Direct GitHub Integration
1. **Fork/Clone** this repository to your GitHub account
2. **Connect to Netlify**:
   - Go to [Netlify](https://netlify.com) → New site from Git
   - Connect your GitHub repository
   - Build settings are automatically configured via `netlify.toml`

#### Option 2: Manual Deployment
1. **Build command**: `python deploy.py`
2. **Publish directory**: `.`
3. **Runtime**: Python 3.9 (specified in `runtime.txt`)

### ⚙️ Environment Configuration

The app automatically configures itself for deployment with:
- **Streamlit config** optimized for production
- **PWA manifest** for mobile installation
- **Service worker** for offline functionality
- **Netlify redirects** for SPA routing

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
