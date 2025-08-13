import streamlit as st
import re
import numpy as np
from collections import Counter

# Page config with white background
st.set_page_config(
    page_title="Resume RAG Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for white background and clean styling
st.markdown("""
<style>
    .stApp {
        background-color: white;
    }
    .main .block-container {
        background-color: white;
        padding-top: 2rem;
    }
    .stButton > button {
        background-color: #007ACC;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    .stButton > button:hover {
        background-color: #005A9E;
    }
    .instruction-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #007ACC;
        margin: 1rem 0;
    }
    .example-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'documents' not in st.session_state:
    st.session_state.documents = []
if 'document_keywords' not in st.session_state:
    st.session_state.document_keywords = []

# Header
st.title("🤖 Resume RAG Chatbot")
st.markdown("**AI-Powered Resume Analysis & Candidate Screening Tool**")

# How to use instructions
st.markdown("""
<div class="instruction-box">
<h3>📋 How to Use This App</h3>
<ol>
<li><strong>Upload Multiple Resumes:</strong> Use the file uploader below to upload multiple resume files (TXT format)</li>
<li><strong>Process Content:</strong> Click the "Process Resumes" button to analyze and index all uploaded content</li>
<li><strong>Ask Questions:</strong> Use natural language to ask specific questions about candidates</li>
<li><strong>Get Precise Answers:</strong> The AI will search through all resumes and provide targeted information</li>
</ol>
</div>
""", unsafe_allow_html=True)

# Extract keywords from text
def extract_keywords(text):
    text = text.lower()
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text)
    stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'who', 'boy', 'did', 'she', 'use', 'way', 'many', 'sit', 'set', 'run', 'eat', 'far', 'sea', 'eye', 'ask', 'try', 'own', 'say', 'too', 'any', 'put', 'end', 'why', 'let', 'cut'}
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    return keywords

# Calculate relevance score
def calculate_relevance_score(query_keywords, doc_keywords):
    if not query_keywords or not doc_keywords:
        return 0
    
    query_counter = Counter(query_keywords)
    doc_counter = Counter(doc_keywords)
    
    score = 0
    for word, count in query_counter.items():
        if word in doc_counter:
            score += count * doc_counter[word]
    
    return score / (len(query_keywords) * len(doc_keywords))

# Extract specific information
def extract_specific_info(text, query):
    query_lower = query.lower()
    text_lower = text.lower()
    
    # Phone number patterns
    if any(keyword in query_lower for keyword in ['phone', 'mobile', 'telephone', 'contact number', 'number']):
        phone_patterns = [
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            r'\(\d{3}\)\s*\d{3}[-.]?\d{4}\b',
            r'\+\d{1,3}[-.]?\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        ]
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            if matches:
                return f"Phone number: {matches[0]}"
    
    # Email patterns
    if any(keyword in query_lower for keyword in ['email', 'mail', 'contact']):
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            return f"Email: {emails[0]}"
    
    # Skills patterns
    if any(keyword in query_lower for keyword in ['skill', 'technology', 'programming', 'language']):
        skills_keywords = ['python', 'java', 'javascript', 'react', 'node', 'sql', 'html', 'css', 'machine learning', 'ai', 'data science', 'aws', 'docker', 'kubernetes']
        found_skills = []
        for skill in skills_keywords:
            if skill in text_lower:
                found_skills.append(skill)
        if found_skills:
            return f"Skills found: {', '.join(found_skills)}"
    
    return None

# Main search and answer function
def search_and_answer(query, documents):
    query_keywords = extract_keywords(query)
    
    # Try specific info extraction first
    for doc in documents:
        specific_info = extract_specific_info(doc, query)
        if specific_info:
            return specific_info
    
    # Fallback to keyword search
    best_score = 0
    best_answer = ""
    
    for doc in documents:
        doc_keywords = extract_keywords(doc)
        score = calculate_relevance_score(query_keywords, doc_keywords)
        
        if score > best_score:
            best_score = score
            sentences = doc.split('.')
            relevant_sentences = []
            for sentence in sentences:
                if any(keyword in sentence.lower() for keyword in query_keywords):
                    relevant_sentences.append(sentence.strip())
            
            if relevant_sentences:
                best_answer = '. '.join(relevant_sentences[:3])
    
    return best_answer if best_answer else "Information not found in the uploaded resumes."

# File upload section - Focus on multiple resumes
st.markdown("### 📁 Upload Multiple Resume Files")
st.markdown("Upload text files containing resume content. You can upload multiple files at once for batch analysis.")

uploaded_files = st.file_uploader(
    "Choose resume files (TXT format)", 
    type=['txt'], 
    accept_multiple_files=True,
    help="Select multiple .txt files containing resume content. Each file should contain one complete resume."
)

# Process files
if uploaded_files:
    if st.button("🔄 Process Resumes", type="primary"):
        with st.spinner("🔍 Processing and analyzing resume content..."):
            all_texts = []
            
            # Process uploaded files
            for file in uploaded_files:
                text = str(file.read(), "utf-8")
                all_texts.append(text)
            
            # Store in session state
            st.session_state.documents = all_texts
            
            # Extract keywords
            all_keywords = []
            for text in all_texts:
                keywords = extract_keywords(text)
                all_keywords.extend(keywords)
            st.session_state.document_keywords = all_keywords
            
            st.success(f"✅ Successfully processed {len(all_texts)} resume(s)! Ready for questions.")
            st.info(f"📊 Indexed {len(all_keywords)} keywords from all resumes.")

# Query section with enhanced UI
if st.session_state.documents:
    st.markdown("---")
    st.markdown("### 💬 Ask Questions About Candidates")
    st.markdown("Use natural language to ask specific questions about the uploaded resumes.")
    
    # Example prompts in a nice box
    st.markdown("""
    <div class="example-box">
    <h4>💡 Example Questions You Can Ask:</h4>
    <ul>
        <li><strong>Contact Information:</strong> "What is John's phone number?" or "Give me Sarah's email address"</li>
        <li><strong>Skills & Technologies:</strong> "Who has Python experience?" or "List candidates with machine learning skills"</li>
        <li><strong>Experience:</strong> "Who has the most years of experience?" or "Find candidates with 5+ years experience"</li>
        <li><strong>Education:</strong> "Who has a computer science degree?" or "List candidates with MBA"</li>
        <li><strong>Comparison:</strong> "Compare the programming skills of all candidates"</li>
        <li><strong>Specific Roles:</strong> "Who is best suited for a data scientist position?"</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Main question input
    col1, col2 = st.columns([4, 1])
    
    with col1:
        query = st.text_input(
            "🔍 Enter your question:",
            placeholder="e.g., 'Who has Python and React experience?' or 'What is the email of the candidate with 5+ years experience?'",
            help="Ask specific questions about candidates. Be as detailed as possible for better results."
        )
    
    with col2:
        search_button = st.button("🔍 Search", type="primary", use_container_width=True)
    
    # Process query
    if query and (search_button or query):
        with st.spinner("🔍 Searching through all resumes..."):
            answer = search_and_answer(query, st.session_state.documents)
            
            # Display results
            st.markdown("#### 🎯 Answer:")
            if answer and answer != "Information not found in the uploaded resumes.":
                st.success(answer)
            else:
                st.warning("❌ Information not found in the uploaded resumes.")
                st.info("💡 Try rephrasing your question or asking for different information.")
            
            # Advanced options
            with st.expander("🔧 Advanced Options"):
                show_sources = st.checkbox("Show source documents")
                if show_sources:
                    st.markdown("**📄 Source Documents:**")
                    for i, doc in enumerate(st.session_state.documents):
                        with st.container():
                            st.markdown(f"**Resume {i+1}:**")
                            st.text_area(f"Content {i+1}", doc[:1000] + "..." if len(doc) > 1000 else doc, height=200, key=f"doc_{i}")

else:
    # Instructions when no documents uploaded
    st.markdown("---")
    st.markdown("""
    <div class="instruction-box">
    <h3>👆 Start by uploading resume files above</h3>
    <p>Upload multiple resume files (in TXT format) to begin analyzing candidate information. Once uploaded, you'll be able to ask detailed questions about:</p>
    <ul>
        <li>Contact information (phone, email, address)</li>
        <li>Skills and technologies</li>
        <li>Work experience and years</li>
        <li>Education background</li>
        <li>Specific qualifications</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("🤖 **Resume RAG Chatbot**")
with col2:
    st.markdown("⚡ **AI-Powered Search**")
with col3:
    st.markdown("📄 **Multi-Resume Analysis**")