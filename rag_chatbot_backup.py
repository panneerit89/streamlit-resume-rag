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
        color: black;
    }
    .main .block-container {
        background-color: white;
        padding-top: 2rem;
        color    # Pr      # Search button with enhanced styling
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        search_clicked = st.button("🔍 Search Resumes with AI", type="primary", use_container_width=True)
    
    # Process question when submitted
    if question and search_clicked:
        with st.spinner("🤖 AI is analyzing resumes and processing your question..."):
            answer = search_and_answer(question, st.session_state.documents)
            
            if answer and answer != "Information not found in the uploaded resumes.":
                st.markdown("### 📋 AI Search Results")
                st.success(answer)
                
                # Show additional details
                with st.expander("📊 Search Details"):
                    st.info(f"**Question:** {question}")
                    st.info(f"**Documents analyzed:** {len(st.session_state.documents)} resume(s)")
                    st.info(f"**Total keywords extracted:** {len(st.session_state.get('keywords', []))} terms")
            else:
                st.warning("⚠️ No relevant information found for your question.")
                st.markdown("""
                **Tips for better results:**
                - Be more specific about skills or requirements
                - Try different keywords or phrases  
                - Ask about concrete experience or qualifications
                - Check the example questions below for ideas
                """)

    # Example questions in an expander
    with st.expander("💡 Example Questions"):
        st.markdown("""
        **Skills & Technology:**
        - Which candidates have Python programming experience?
        - Who has worked with machine learning or AI?
        - Which applicants have cloud computing experience?
        
        **Experience & Background:**
        - Who has more than 5 years of experience?
        - Which candidates have startup experience?
        - Who has led a team or managed projects?
        
        **Education & Certifications:**
        - Which candidates have computer science degrees?
        - Who has relevant certifications?
        - Which applicants have advanced degrees?
        """)
        color: black !important;
    }
    div[data-testid="stFileUploader"] label {
        color: black !important;
    }
    
    /* Button styling */
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
    
    /* AGGRESSIVE File uploader styling - override Streamlit defaults */
    .stFileUploader {
        background-color: white !important;
    }
    
    .stFileUploader > div {
        background-color: #f8f9fa !important;
        border: 2px dashed #007ACC !important;
        border-radius: 10px !important;
        padding: 2rem !important;
        text-align: center !important;
        color: black !important;
    }
    
    .stFileUploader > div:hover {
        background-color: #e8f4fd !important;
        border-color: #005A9E !important;
    }
    
    /* Target ALL possible file uploader elements */
    div[data-testid="stFileUploader"] {
        background-color: white !important;
    }
    
    div[data-testid="stFileUploader"] > div {
        background-color: #f8f9fa !important;
        border: 2px dashed #007ACC !important;
        border-radius: 10px !important;
        color: black !important;
    }
    
    div[data-testid="stFileUploaderDropzone"] {
        background-color: #f8f9fa !important;
        border: 2px dashed #007ACC !important;
        border-radius: 10px !important;
        color: black !important;
        padding: 2rem !important;
    }
    
    div[data-testid="stFileUploaderDropzone"] * {
        background-color: transparent !important;
        color: black !important;
    }
    
    /* Override any nested divs in file uploader */
    .stFileUploader div, .stFileUploader div div, .stFileUploader div div div {
        background-color: #f8f9fa !important;
        color: black !important;
    }
    
    /* Force override for the main dropzone area */
    section[data-testid="stFileUploader"] div {
        background-color: #f8f9fa !important;
        color: black !important;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        background-color: white;
        border: 1px solid #007ACC;
        border-radius: 5px;
        color: black;
        padding: 0.5rem;
    }
    .stTextInput > div > div > input:focus {
        border-color: #005A9E;
        box-shadow: 0 0 0 2px rgba(0, 122, 204, 0.2);
    }
    
    /* Text area styling */
    .stTextArea > div > div > textarea {
        background-color: white;
        border: 1px solid #007ACC;
        border-radius: 5px;
        color: black;
        padding: 0.5rem;
    }
    
    /* Success/Info/Warning styling */
    .stSuccess {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .stInfo {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
    .stWarning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        color: black !important;
    }
    .streamlit-expanderContent {
        background-color: white;
        color: black !important;
    }
    
    /* Instruction and example boxes */
    .instruction-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #007ACC;
        margin: 1rem 0;
        color: black !important;
    }
    .instruction-box h3, .instruction-box p, .instruction-box li {
        color: black !important;
    }
    
    .example-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: black !important;
    }
    .example-box h4, .example-box p, .example-box li {
        color: black !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
        color: black;
    }
    
    /* Column styling */
    .css-1kyxreq {
        color: black !important;
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

# Additional CSS specifically for file uploader after the element is created
st.markdown("""
<style>
/* FINAL OVERRIDE for file uploader - highest specificity */
div[data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzone"] {
    background: linear-gradient(to bottom, #f8f9fa, #f8f9fa) !important;
    background-color: #f8f9fa !important;
    border: 2px dashed #007ACC !important;
    border-radius: 10px !important;
    color: black !important;
    padding: 2rem !important;
}

div[data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzone"]:hover {
    background: linear-gradient(to bottom, #e8f4fd, #e8f4fd) !important;
    background-color: #e8f4fd !important;
    border-color: #005A9E !important;
}

/* Force all nested elements in file uploader to be light */
div[data-testid="stFileUploader"] * {
    background-color: transparent !important;
    color: black !important;
}

div[data-testid="stFileUploader"] div {
    background-color: #f8f9fa !important;
}
</style>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Choose resume files (TXT format)", 
    type=['txt'], 
    accept_multiple_files=True,
    help="Select multiple .txt files containing resume content. Each file should contain one complete resume."
)

# Add neat box styling specifically for the file uploader
st.markdown("""
<style>
/* Create a beautiful, neat file uploader box */
section[data-testid="stFileUploaderDropzone"] {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%) !important;
    border: 2px dashed #007bff !important;
    border-radius: 15px !important;
    box-shadow: 0 4px 15px rgba(0,123,255,0.15) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    padding: 25px !important;
    position: relative !important;
    overflow: hidden !important;
    margin-bottom: 10px !important;
}

/* Reduce spacing between elements */
.stElementContainer {
    margin-bottom: 0.5rem !important;
}

/* Override the specific emotion cache class that's causing dark background */
.st-emotion-cache-mcvmo3 {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%) !important;
    border: 2px dashed #007bff !important;
    border-radius: 15px !important;
    box-shadow: 0 4px 15px rgba(0,123,255,0.15) !important;
}

/* Style all text in the dropzone with elegant typography */
section[data-testid="stFileUploaderDropzone"] * {
    color: #2c3e50 !important;
    font-weight: 500 !important;
}

/* Beautiful gradient button */
section[data-testid="stFileUploaderDropzone"] button {
    background: linear-gradient(135deg, #007bff 0%, #0056b3 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 12px rgba(0,123,255,0.3) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
</style>
""", unsafe_allow_html=True)

# Show uploaded files status
if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully!")
    
    # Process button - prominently displayed
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Process Resumes", type="primary", use_container_width=True):
            with st.spinner("🔍 Processing and analyzing resume content..."):
                all_texts = []
                
                # Process uploaded files
                for file in uploaded_files:
                    text = str(file.read(), "utf-8")
                    all_texts.append(text)
                
                # Store in session state
                st.session_state.documents = all_texts
                
                # Extract keywords from all documents
                all_keywords = set()
                for text in all_texts:
                    keywords = extract_keywords(text)
                    all_keywords.update(keywords)
                
                st.session_state.keywords = list(all_keywords)
                st.session_state.processed = True
                
                st.success(f"✅ Successfully processed {len(all_texts)} resumes with {len(all_keywords)} unique keywords!")
                st.balloons()

# Question interface - only show after processing
if st.session_state.get('processed', False):
    st.markdown("---")
    st.markdown("### 💬 Ask Questions About the Resumes")
    
    # Question input with better styling
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #007bff; margin: 15px 0;">
        <h4 style="color: #007bff; margin-top: 0;">🤖 Ask Your Question</h4>
        <p style="color: #333; margin-bottom: 0;">Ask natural language questions about the candidates' skills, experience, or qualifications.</p>
    </div>
    """, unsafe_allow_html=True)
    
    question = st.text_area(
        "Enter your question here:",
        placeholder="Example: Which candidates have Python and machine learning experience? Who has more than 5 years of experience?",
        help="Ask detailed questions about skills, experience, education, or any specific requirements you need",
        height=100,
        key="user_question"
    )
    
    # Example questions in an expander
    with st.expander("💡 Example Questions"):
        st.markdown("""
        **Skills & Technology:**
        - Which candidates have Python programming experience?
        - Who has worked with machine learning or AI?
        - Which applicants have cloud computing experience?
        
        **Experience & Background:**
        - Who has more than 5 years of experience?
        - Which candidates have startup experience?
        - Who has led a team or managed projects?
        
        **Education & Certifications:**
        - Which candidates have computer science degrees?
        - Who has relevant certifications?
        - Which applicants have advanced degrees?
        """)
    
    # Process question when submitted
    if question and st.button("� Search Resumes", type="secondary"):
        with st.spinner("🔍 Searching through resumes..."):
            answer = search_and_answer(question, st.session_state.documents, st.session_state.keywords)
            
            if answer:
                st.markdown("### 📋 Search Results")
                st.markdown(answer)
            else:
                st.warning("⚠️ No relevant information found for your question. Try rephrasing or asking about different topics.")

else:
    if uploaded_files:
        st.info("👆 Click 'Process Resumes' button above to analyze the uploaded files before asking questions.")
    else:
        st.info("📁 Please upload resume files first, then process them to start asking questions.")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("🤖 **Resume RAG Chatbot**")
with col2:
    st.markdown("⚡ **AI-Powered Search**")
with col3:
    st.markdown("📄 **Multi-Resume Analysis**")