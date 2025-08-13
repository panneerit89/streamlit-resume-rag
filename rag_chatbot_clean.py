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
        padding: 2rem;
    }
    
    /* Neat file uploader styling */
    div[data-testid="stFileUploader"] {
        background: linear-gradient(145deg, #f8f9fa, #e9ecef);
        border: 2px dashed #6c757d;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    div[data-testid="stFileUploader"]:hover {
        border-color: #007bff;
        background: linear-gradient(145deg, #e3f2fd, #bbdefb);
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    div[data-testid="stFileUploader"] label {
        font-weight: 600;
        color: #495057;
        font-size: 1.1rem;
    }
    
    /* Text area styling */
    .stTextArea textarea {
        border: 2px solid #dee2e6;
        border-radius: 10px;
        padding: 1rem;
        background-color: #f8f9fa;
        transition: border-color 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: #007bff;
        box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'documents' not in st.session_state:
    st.session_state.documents = []
if 'keywords' not in st.session_state:
    st.session_state.keywords = []

def extract_text_from_file(file):
    """Extract text content from uploaded file."""
    content = file.read()
    if file.type == "text/plain":
        return content.decode('utf-8')
    elif file.type == "application/pdf":
        # For PDF files, you'd need PyPDF2 or similar
        # For now, returning a placeholder
        return "PDF processing not implemented yet. Please upload text files."
    else:
        return content.decode('utf-8', errors='ignore')

def extract_keywords(text):
    """Extract relevant keywords from text using basic NLP."""
    # Common technical skills and keywords
    skill_patterns = [
        r'\b(?:python|java|javascript|react|angular|vue|node\.js|django|flask)\b',
        r'\b(?:sql|mysql|postgresql|mongodb|redis|elasticsearch)\b',
        r'\b(?:aws|azure|gcp|docker|kubernetes|jenkins|git)\b',
        r'\b(?:machine learning|deep learning|ai|data science|analytics)\b',
        r'\b(?:project manager|team lead|senior|junior|intern)\b',
        r'\b(?:bachelor|master|phd|degree|certification|certified)\b'
    ]
    
    keywords = []
    text_lower = text.lower()
    
    for pattern in skill_patterns:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        keywords.extend(matches)
    
    # Extract years of experience
    exp_pattern = r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)'
    exp_matches = re.findall(exp_pattern, text_lower)
    for exp in exp_matches:
        keywords.append(f"{exp} years experience")
    
    return list(set(keywords))

def search_documents(query, documents, keywords):
    """Search through documents using keyword matching."""
    if not documents:
        return []
    
    query_lower = query.lower()
    results = []
    
    for i, doc in enumerate(documents):
        doc_lower = doc.lower()
        score = 0
        
        # Direct text matching
        if query_lower in doc_lower:
            score += 10
        
        # Keyword matching
        query_words = re.findall(r'\b\w+\b', query_lower)
        for word in query_words:
            if word in doc_lower:
                score += 1
        
        if score > 0:
            results.append({
                'document_index': i,
                'score': score,
                'preview': doc[:200] + "..." if len(doc) > 200 else doc
            })
    
    # Sort by score
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:5]  # Top 5 results

# Main app
st.title("🤖 Resume RAG Chatbot")
st.markdown("Upload resumes and ask questions to find the best candidates!")

# File upload section
st.header("📄 Upload Resume Files")
uploaded_files = st.file_uploader(
    "Choose resume files (PDF, TXT)",
    type=['pdf', 'txt'],
    accept_multiple_files=True,
    help="Upload multiple resume files to analyze and search through them"
)

if uploaded_files:
    if st.button("📊 Process Documents", type="primary"):
        with st.spinner("Processing documents..."):
            st.session_state.documents = []
            st.session_state.keywords = []
            
            for file in uploaded_files:
                text = extract_text_from_file(file)
                st.session_state.documents.append(text)
                keywords = extract_keywords(text)
                st.session_state.keywords.extend(keywords)
            
            st.session_state.keywords = list(set(st.session_state.keywords))
            
        st.success(f"✅ Processed {len(uploaded_files)} documents successfully!")
        st.info(f"📊 Extracted {len(st.session_state.keywords)} unique keywords")

# Question interface
if st.session_state.documents:
    st.header("💬 Ask Questions About the Resumes")
    
    # Text area for questions
    user_question = st.text_area(
        "Enter your question:",
        placeholder="e.g., Which candidates have Python experience? Who has more than 5 years of experience?",
        height=100
    )
    
    if st.button("🔍 Search", type="primary"):
        if user_question.strip():
            with st.spinner("Searching through resumes..."):
                results = search_documents(user_question, st.session_state.documents, st.session_state.keywords)
            
            if results:
                st.success(f"Found {len(results)} relevant matches!")
                
                for i, result in enumerate(results, 1):
                    with st.expander(f"📋 Resume #{result['document_index'] + 1} (Score: {result['score']})"):
                        st.write(result['preview'])
                
                # Show statistics
                st.info(f"**Documents analyzed:** {len(st.session_state.documents)} resume(s)")
                st.info(f"**Total keywords extracted:** {len(st.session_state.keywords)} terms")
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

    # Keywords overview
    if st.session_state.keywords:
        with st.expander("🔍 Extracted Keywords"):
            keyword_counts = Counter(st.session_state.keywords)
            st.write("Most common keywords found:")
            for keyword, count in keyword_counts.most_common(20):
                st.write(f"• {keyword} ({count} mentions)")

else:
    st.info("👆 Please upload resume files first to start asking questions!")

# Footer
st.markdown("---")
st.markdown("💡 **Tip:** Upload multiple resumes in different formats to get better search results!")
