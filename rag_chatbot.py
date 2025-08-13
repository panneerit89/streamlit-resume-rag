import streamlit as st
import os
import tempfile
import numpy as np
import re
import io
from collections import Counter
import math

# ChatGPT-5 inspired styling with dark theme + PWA support
st.set_page_config(
    page_title="Resume RAG Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# PWA Configuration and Meta Tags
st.markdown("""
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#64ffda">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Resume RAG">
    <meta name="description" content="AI-powered resume analysis and candidate screening chatbot">
    <meta name="keywords" content="resume, AI, chatbot, recruitment, screening">
    
    <!-- PWA Manifest -->
    <link rel="manifest" href="./manifest.json">
    
    <!-- Apple Touch Icons -->
    <link rel="apple-touch-icon" href="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTkyIiBoZWlnaHQ9IjE5MiIgdmlld0JveD0iMCAwIDE5MiAxOTIiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3Qgd2lkdGg9IjE5MiIgaGVpZ2h0PSIxOTIiIHJ4PSIyNCIgZmlsbD0idXJsKCNncmFkaWVudDApIi8+PHBhdGggZD0iTTk2IDQ4Qzc0LjQgNDggNTYgNjYuNCA1NiA4OFYxMjhDNTYgMTM2LjggNjMuMiAxNDQgNzIgMTQ0SDEyMEMxMjguOCAxNDQgMTM2IDEzNi44IDEzNiAxMjhWODhDMTM2IDY2LjQgMTE3LjYgNDggOTYgNDhaIiBmaWxsPSIjNjRmZmRhIi8+PC9zdmc+">
    
    <!-- Service Worker Registration -->
    <script>
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', function() {
                navigator.serviceWorker.register('./sw.js')
                .then(function(registration) {
                    console.log('ServiceWorker registration successful');
                }, function(err) {
                    console.log('ServiceWorker registration failed: ', err);
                });
            });
        }
    </script>
</head>
""", unsafe_allow_html=True)

# Custom CSS for ChatGPT-5 inspired desi        <div style="font-size: 4rem; margin-bottom: 1rem;">🚀</div>n
st.markdown("""
<style>
    /* Main background - ChatGPT-5 dark theme */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: #e5e5e5;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 90%;
    }
    
    /* Title styling */
    .main-title {
        background: linear-gradient(90deg, #64ffda, #00bcd4, #0096c7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
        font-family: 'Inter', sans-serif;
    }
    
    .subtitle {
        text-align: center;
        color: #a0a0a0;
        font-size: 1.3rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Card styling */
    .info-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .feature-card {
        background: linear-gradient(135deg, rgba(100, 255, 218, 0.1), rgba(0, 188, 212, 0.1));
        border: 1px solid rgba(100, 255, 218, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(100, 255, 218, 0.2);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #64ffda, #00bcd4);
        color: #0f0f23;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(100, 255, 218, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(100, 255, 218, 0.4);
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        background: rgba(255, 255, 255, 0.05);
        border: 2px dashed rgba(100, 255, 218, 0.3);
        border-radius: 12px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div:hover {
        border-color: rgba(100, 255, 218, 0.6);
        background: rgba(100, 255, 218, 0.05);
    }
    
    /* Text input styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(100, 255, 218, 0.3);
        border-radius: 8px;
        color: #e5e5e5;
        font-size: 1.1rem;
        padding: 0.75rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #64ffda;
        box-shadow: 0 0 0 2px rgba(100, 255, 218, 0.2);
    }
    
    /* Success/info/warning styling */
    .stSuccess {
        background: linear-gradient(90deg, rgba(76, 175, 80, 0.1), rgba(139, 195, 74, 0.1));
        border-left: 4px solid #4caf50;
        color: #81c784;
    }
    
    .stInfo {
        background: linear-gradient(90deg, rgba(33, 150, 243, 0.1), rgba(100, 255, 218, 0.1));
        border-left: 4px solid #64ffda;
        color: #64ffda;
    }
    
    .stWarning {
        background: linear-gradient(90deg, rgba(255, 152, 0, 0.1), rgba(255, 193, 7, 0.1));
        border-left: 4px solid #ff9800;
        color: #ffb74d;
    }
    
    /* Markdown styling */
    .stMarkdown h3 {
        color: #64ffda;
        font-weight: 600;
        border-bottom: 2px solid rgba(100, 255, 218, 0.2);
        padding-bottom: 0.5rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(15, 15, 35, 0.9);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(100, 255, 218, 0.1);
        border-radius: 8px;
        color: #64ffda;
    }
    
    /* Chat-like styling for answers */
    .chat-response {
        background: linear-gradient(135deg, rgba(100, 255, 218, 0.1), rgba(0, 188, 212, 0.05));
        border-left: 4px solid #64ffda;
        border-radius: 0 12px 12px 0;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        font-size: 1.1rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    }
    
    .ai-icon {
        background: linear-gradient(135deg, #64ffda, #00bcd4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.5rem;
        font-weight: bold;
    }
    
    /* Glassmorphism effect for main containers */
    .glass-container {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Main header with ChatGPT-5 inspired design
st.markdown("""
<div style="text-align: center; margin-bottom: 3rem;">
    <h1 class="main-title">🤖 Resume RAG Chatbot</h1>
    <p class="subtitle">Powered by AI • Upload resumes and ask intelligent questions about candidates</p>
</div>
""", unsafe_allow_html=True)

# Beautiful feature cards for instructions
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div style="text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 3rem; color: #64ffda;">📤</div>
        </div>
        <h4 style="color: #64ffda; text-align: center;">Upload PDFs</h4>
        <p style="text-align: center; color: #a0a0a0;">Drag & drop multiple resume PDFs for AI processing</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div style="text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 3rem; color: #64ffda;">⚡</div>
        </div>
        <h4 style="color: #64ffda; text-align: center;">AI Processing</h4>
        <p style="text-align: center; color: #a0a0a0;">Advanced AI extracts and indexes candidate information</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div style="text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 3rem; color: #64ffda;">💬</div>
        </div>
        <h4 style="color: #64ffda; text-align: center;">Ask Questions</h4>
        <p style="text-align: center; color: #a0a0a0;">Get instant, intelligent answers about candidates</p>
    </div>
    """, unsafe_allow_html=True)

# Example queries section
st.markdown("""
<div class="info-card">
    <h3 style="color: #64ffda; margin-bottom: 1rem;">💡 Example Queries</h3>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
        <div>
            <p style="color: #81c784;">• "Find candidates with Python experience"</p>
            <p style="color: #81c784;">• "Who has machine learning skills?"</p>
        </div>
        <div>
            <p style="color: #81c784;">• "Show me project management experience"</p>
            <p style="color: #81c784;">• "List candidates with 5+ years experience"</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize session state for documents and search
if "documents" not in st.session_state:
    st.session_state.documents = []
if "document_keywords" not in st.session_state:
    st.session_state.document_keywords = []
if "chunks" not in st.session_state:
    st.session_state.chunks = []
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

# Function to extract text from uploaded file
def extract_text_from_file(uploaded_file):
    try:
        # Read text file content
        text = uploaded_file.read().decode('utf-8')
        return text
    except Exception as e:
        st.error(f"Error reading file {uploaded_file.name}: {str(e)}")
        return ""

# Function to split text into chunks
def split_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    return chunks

# Function to extract keywords from text
def extract_keywords(text):
    """Extract important keywords from text for simple matching"""
    # Convert to lowercase and remove special characters
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    words = text.split()
    
    # Remove common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'}
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    
    return keywords

# Simple TF-IDF-like scoring for keyword search
def calculate_relevance_score(query_keywords, document_keywords):
    """Calculate relevance score between query and document keywords"""
    if not query_keywords or not document_keywords:
        return 0
    
    query_counter = Counter(query_keywords)
    doc_counter = Counter(document_keywords)
    
    score = 0
    for word, query_freq in query_counter.items():
        if word in doc_counter:
            score += query_freq * doc_counter[word]
    
    # Normalize by document length
    if len(document_keywords) > 0:
        score = score / math.sqrt(len(document_keywords))
    
    return score

# Load sentence transformer model - replaced with simple keyword matching
def simple_keyword_search(query, documents, chunks):
    """Simple keyword-based search without external dependencies"""
    query_keywords = extract_keywords(query)
    
    # Search through all text
    all_text = "\n".join(documents)
    
    # Find relevant chunks based on keyword overlap
    chunk_scores = []
    for i, chunk in enumerate(chunks):
        chunk_keywords = extract_keywords(chunk)
        score = calculate_relevance_score(query_keywords, chunk_keywords)
        chunk_scores.append((score, chunk))
    
    # Sort by relevance score
    chunk_scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return top 3 most relevant chunks
    relevant_chunks = [chunk for score, chunk in chunk_scores[:3] if score > 0]
    
    return relevant_chunks if relevant_chunks else [all_text[:1000]]  # Fallback to first 1000 chars

# File uploader section with enhanced styling
st.markdown("""
<div class="glass-container">
    <h3 style="color: #64ffda; margin-bottom: 1.5rem; text-align: center;">
    <h3 style="color: #64ffda; margin-bottom: 1.5rem; text-align: center;">
        <span style="font-size: 2rem;">📁</span> Upload Resume Files
    </h3>
    <p style="text-align: center; color: #a0a0a0; margin-bottom: 2rem;">
        Upload text files with resume content or paste resume text directly
    </p>
""", unsafe_allow_html=True)

# Text area for direct input
resume_text = st.text_area(
    "Paste resume content here:",
    height=200,
    placeholder="Copy and paste resume text here...",
    help="You can paste the text content of resumes directly here for processing."
)

# File uploader for text files
uploaded_files = st.file_uploader(
    "Or upload text files", 
    type=["txt", "md"], 
    accept_multiple_files=True,
    help="You can upload multiple text files containing resume content.",
    label_visibility="collapsed"
)

st.markdown("</div>", unsafe_allow_html=True)

# Process uploaded files or direct text input
if uploaded_files or resume_text.strip():
    new_files = []
    if uploaded_files:
        new_files = [f for f in uploaded_files if f.name not in st.session_state.uploaded_files]
    
    has_new_content = bool(new_files) or (resume_text.strip() and "direct_input" not in st.session_state.uploaded_files)
    
    if has_new_content:
        if new_files:
            st.session_state.uploaded_files.extend([f.name for f in new_files])
        if resume_text.strip() and "direct_input" not in st.session_state.uploaded_files:
            st.session_state.uploaded_files.append("direct_input")
        
        # Beautiful processing indicator
        st.markdown("""
        <div style="background: rgba(100, 255, 218, 0.1); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(100, 255, 218, 0.3); margin: 1rem 0;">
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <div style="font-size: 2rem; margin-right: 1rem;">⚡</div>
                <h4 style="color: #64ffda; margin: 0;">Processing resume content...</h4>
            </div>
            <div style="color: #a0a0a0;">AI is extracting and indexing candidate information for intelligent search</div>
        </div>
        """, unsafe_allow_html=True)

        # Process content
        all_texts = []
        all_chunks = []
        
        # Process direct text input
        if resume_text.strip():
            all_texts.append(resume_text.strip())
            chunks = split_text(resume_text.strip())
            all_chunks.extend(chunks)
        
        # Process uploaded files
        for uploaded_file in new_files:
            text = extract_text_from_file(uploaded_file)
            if text:
                all_texts.append(text)
                chunks = split_text(text)
                all_chunks.extend(chunks)
        
        # Store documents in session state
        st.session_state.documents.extend(all_texts)
        st.session_state.chunks.extend(all_chunks)
        
        # Extract keywords for simple search
        all_keywords = []
        for text in all_texts:
            keywords = extract_keywords(text)
            all_keywords.extend(keywords)
        
        st.session_state.document_keywords.extend(all_keywords)
        
        # Beautiful success message
        st.markdown("""
        <div style="background: linear-gradient(90deg, rgba(76, 175, 80, 0.2), rgba(139, 195, 74, 0.2)); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #4caf50; margin: 1rem 0;">
            <div style="display: flex; align-items: center;">
                <div style="font-size: 2rem; margin-right: 1rem;">✅</div>
                <div>
                    <h4 style="color: #81c784; margin: 0;">Resume content processed successfully!</h4>
                    <p style="color: #a0a0a0; margin: 0.5rem 0 0 0;">Your content is now ready for intelligent querying</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Simple pattern-based answer extraction
def extract_specific_info(text, query):
    """Extract specific information from text based on query patterns"""
    query_lower = query.lower()
    text_lower = text.lower()
    
    # Phone number patterns - more comprehensive
    if any(keyword in query_lower for keyword in ['phone', 'mobile', 'telephone', 'contact number', 'number']):
        phone_patterns = [
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # 123-456-7890 or 1234567890
            r'\(\d{3}\)\s*\d{3}[-.]?\d{4}',    # (123) 456-7890
            r'\+\d{1,3}[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',  # +1-123-456-7890
            r'\b\d{10}\b',  # 1234567890
            r'\d{3}\s\d{3}\s\d{4}',  # 123 456 7890
        ]
        
        # First try to find phone numbers in lines that mention contact info
        contact_lines = []
        for line in text.split('\n'):
            if any(word in line.lower() for word in ['phone', 'mobile', 'contact', 'tel', 'call']):
                contact_lines.append(line)
        
        # Search in contact-specific lines first
        for line in contact_lines:
            for pattern in phone_patterns:
                matches = re.findall(pattern, line)
                if matches:
                    return matches[0]
        
        # If not found in contact lines, search entire text
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0]
    
    # Email patterns - more robust
    if any(keyword in query_lower for keyword in ['email', 'mail', '@']):
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        # Search in email-specific lines first
        email_lines = []
        for line in text.split('\n'):
            if any(word in line.lower() for word in ['email', 'mail', '@']):
                email_lines.append(line)
        
        for line in email_lines:
            matches = re.findall(email_pattern, line)
            if matches:
                return matches[0]
        
        # Search entire text
        matches = re.findall(email_pattern, text)
        if matches:
            return matches[0]
    
    # Address patterns
    if any(keyword in query_lower for keyword in ['address', 'location', 'city', 'state']):
        # Look for address-like patterns
        address_patterns = [
            r'\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd)',
            r'[A-Za-z\s]+,\s*[A-Z]{2}\s*\d{5}'  # City, ST 12345
        ]
        for pattern in address_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return matches[0]
    
    # Skills patterns - improved
    if any(keyword in query_lower for keyword in ['skill', 'technology', 'programming', 'language']):
        # Common programming languages and technologies
        tech_keywords = ['python', 'java', 'javascript', 'react', 'angular', 'node.js', 'sql', 
                        'machine learning', 'ai', 'data science', 'aws', 'docker', 'kubernetes',
                        'c++', 'c#', 'html', 'css', 'git', 'linux', 'windows', 'excel']
        found_skills = []
        for skill in tech_keywords:
            if skill in text_lower:
                found_skills.append(skill.title())
        if found_skills:
            return ', '.join(found_skills[:5])  # Limit to 5 skills
    
    # Experience patterns - more comprehensive
    if any(keyword in query_lower for keyword in ['experience', 'years', 'work']):
        exp_patterns = [
            r'(\d+)\s+years?\s+(?:of\s+)?experience',
            r'(\d+)\s*\+?\s*years?\s+(?:in|with|of)',
            r'experience.*?(\d+)\s+years?',
        ]
        for pattern in exp_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                return f"{matches[0]} years of experience"
    
    return None

# Simple search and answer function using keyword matching
def search_and_answer(query):
    """Search documents and provide precise answers using keyword matching"""
    if len(st.session_state.documents) == 0:
        return "Please upload some resume content or paste text first."
    
    query_lower = query.lower()
    
    # Get all text from documents
    all_text = "\n".join(st.session_state.documents)
    
    # For contact info queries, be very specific
    if any(keyword in query_lower for keyword in ['phone', 'number', 'contact', 'telephone', 'mobile']):
        # Look for phone numbers anywhere in the text
        phone_patterns = [
            r'\+?1?[-.\s]?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})',  # Various formats
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            r'\(\d{3}\)\s*\d{3}[-.]?\d{4}',
            r'\b\d{10}\b'
        ]
        
        for pattern in phone_patterns:
            matches = re.findall(pattern, all_text)
            if matches:
                if isinstance(matches[0], tuple):
                    # For grouped patterns, join the groups
                    return f"({matches[0][0]}) {matches[0][1]}-{matches[0][2]}"
                else:
                    return matches[0]
    
    # For email queries
    if any(keyword in query_lower for keyword in ['email', 'mail']):
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(email_pattern, all_text)
        if matches:
            return matches[0]
    
    # For skills queries
    if any(keyword in query_lower for keyword in ['skill', 'technology', 'programming', 'language']):
        tech_keywords = ['python', 'java', 'javascript', 'react', 'angular', 'node.js', 'sql', 
                        'machine learning', 'ai', 'data science', 'aws', 'docker', 'kubernetes',
                        'c++', 'c#', 'html', 'css', 'git', 'linux', 'windows', 'excel', 'powerbi',
                        'tableau', 'mongodb', 'postgresql', 'mysql', 'django', 'flask', 'pandas',
                        'numpy', 'tensorflow', 'pytorch', 'spark', 'hadoop']
        found_skills = []
        for skill in tech_keywords:
            if skill in all_text.lower():
                found_skills.append(skill.title())
        if found_skills:
            return ', '.join(found_skills[:8])  # Limit to 8 skills
    
    # For experience queries
    if any(keyword in query_lower for keyword in ['experience', 'years', 'work']):
        exp_patterns = [
            r'(\d+)\+?\s+years?\s+(?:of\s+)?experience',
            r'(\d+)\s*\+?\s*years?\s+(?:in|with|of)',
            r'over\s+(\d+)\s+years?',
            r'more than\s+(\d+)\s+years?'
        ]
        for pattern in exp_patterns:
            matches = re.findall(pattern, all_text.lower())
            if matches:
                return f"{matches[0]} years of experience"
    
    # For name queries
    if any(keyword in query_lower for keyword in ['name', 'candidate', 'who']):
        # Look for names at the beginning of documents
        for doc in st.session_state.documents:
            lines = doc.split('\n')[:5]  # Check first 5 lines
            for line in lines:
                line = line.strip()
                # Skip common headers and look for actual names
                if line and not any(skip in line.lower() for skip in ['resume', 'cv', 'curriculum']):
                    # Check if it looks like a name (2-4 words, capitalized)
                    words = line.split()
                    if 2 <= len(words) <= 4 and all(word[0].isupper() for word in words if word.isalpha()):
                        return line
    
    # If no specific pattern matched, do keyword-based search
    try:
        relevant_chunks = simple_keyword_search(query, st.session_state.documents, st.session_state.chunks)
        combined_text = "\n".join(relevant_chunks)
        
        # Return the most relevant short excerpt
        sentences = re.split(r'[.!?]+', combined_text)
        query_words = set(word.lower() for word in query.split() if len(word) > 2)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10:  # Skip very short sentences
                sentence_lower = sentence.lower()
                # Check if sentence contains query words
                if any(word in sentence_lower for word in query_words):
                    return sentence
    except Exception as e:
        st.error(f"Search error: {str(e)}")
    
    return "Information not found in the uploaded content."

# Query interface - check if documents are uploaded
if len(st.session_state.documents) > 0:
    st.markdown("""
    <div class="glass-container">
        <h3 style="color: #64ffda; margin-bottom: 1.5rem; text-align: center;">
            <span class="ai-icon">🤖</span> Ask Questions About Candidates
        </h3>
        <p style="text-align: center; color: #a0a0a0; margin-bottom: 2rem;">
            Ask specific questions for precise answers. Be clear about what information you want.
        </p>
    """, unsafe_allow_html=True)
    
    # Add examples of good queries
    with st.expander("💡 Example Questions for Precise Answers", expanded=False):
        st.markdown("""
        <div style="background: rgba(100, 255, 218, 0.05); padding: 1rem; border-radius: 8px;">
            <h4 style="color: #64ffda;">For specific information:</h4>
            <p style="color: #81c784;">• "What is John's phone number?"</p>
            <p style="color: #81c784;">• "Give me Sarah's email address"</p>
            <p style="color: #81c784;">• "List the programming languages mentioned in Mike's resume"</p>
            
            <h4 style="color: #64ffda; margin-top: 1.5rem;">For comparisons:</h4>
            <p style="color: #81c784;">• "Who has the most years of Python experience?"</p>
            <p style="color: #81c784;">• "Which candidate has machine learning skills?"</p>
            <p style="color: #81c784;">• "Find candidates with project management experience"</p>
        </div>
        """, unsafe_allow_html=True)
    
    # User query input with enhanced styling
    query = st.text_input(
        "Your Question:", 
        placeholder="e.g., 'What is the phone number?' or 'Who has Python skills?'",
        help="Ask specific questions for precise answers. The AI will only provide the information you request."
    )
    
    if query:
        with st.spinner("🔍 Searching for relevant candidate information..."):
            try:
                # Use the new FAISS-based search approach
                answer = search_and_answer(query)
                
                # Show debug info in development
                if st.checkbox("🔧 Show debug info", value=False):
                    st.markdown("**Debug - Uploaded Documents:**")
                    for i, doc in enumerate(st.session_state.documents[:2]):
                        st.code(f"Doc {i+1}: {doc[:200]}...")
                
                # Display answer with beautiful styling
                if answer and answer != "Information not found in the uploaded resumes.":
                    st.markdown(f"""
                    <div class="chat-response">
                        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                            <span class="ai-icon">🤖</span>
                            <span style="margin-left: 0.5rem; color: #64ffda; font-weight: 600;">AI Assistant</span>
                        </div>
                        <p style="margin: 0; font-size: 1.1rem; line-height: 1.6;">{answer}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("🔍 Information not found in the uploaded resumes.")
                    st.info("💡 Try asking for specific information like:\n• Phone number\n• Email address\n• Skills or technologies\n• Years of experience")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
    
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="glass-container" style="text-align: center;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">�</div>
        <h3 style="color: #64ffda; margin-bottom: 1rem;">Ready to Get Started?</h3>
        <p style="color: #a0a0a0; font-size: 1.2rem; margin-bottom: 2rem;">
            Upload at least one resume PDF above to start asking questions about candidates!
        </p>
        
        <div style="background: rgba(100, 255, 218, 0.05); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(100, 255, 218, 0.2);">
            <h4 style="color: #64ffda; margin-bottom: 1rem;">Once you upload resumes, you'll be able to ask:</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; text-align: left;">
                <div>
                    <p style="color: #81c784;">📞 "What is the phone number?"</p>
                    <p style="color: #81c784;">💼 "What skills does the candidate have?"</p>
                </div>
                <div>
                    <p style="color: #81c784;">📧 "What is the email address?"</p>
                    <p style="color: #81c784;">⏰ "How many years of experience?"</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Add a simple footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("🤖 **Resume RAG Chatbot**")
with col2:
    st.markdown("⚡ **Powered by AI**")
with col3:
    st.markdown("🚀 **LangChain • Streamlit**")