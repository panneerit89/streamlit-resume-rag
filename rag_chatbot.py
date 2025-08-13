import streamlit as st
import re
import numpy as np
from collections import Counter

# Simple page config
st.set_page_config(
    page_title="Resume RAG Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'documents' not in st.session_state:
    st.session_state.documents = []
if 'document_keywords' not in st.session_state:
    st.session_state.document_keywords = []

# Simple header
st.title("Resume RAG Chatbot")
st.write("Upload resume text and ask questions to find specific information")

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

# File upload section
st.subheader("Upload Resume Files")
uploaded_files = st.file_uploader(
    "Choose text files", 
    type=['txt'], 
    accept_multiple_files=True
)

# Text input section
st.subheader("Or Paste Resume Text")
text_input = st.text_area("Paste resume content here:", height=200)

# Process files and text
if uploaded_files or text_input:
    if st.button("Process Content"):
        with st.spinner("Processing..."):
            all_texts = []
            
            # Process uploaded files
            if uploaded_files:
                for file in uploaded_files:
                    text = str(file.read(), "utf-8")
                    all_texts.append(text)
            
            # Process text input
            if text_input:
                all_texts.append(text_input)
            
            # Store in session state
            st.session_state.documents = all_texts
            
            # Extract keywords
            all_keywords = []
            for text in all_texts:
                keywords = extract_keywords(text)
                all_keywords.extend(keywords)
            st.session_state.document_keywords = all_keywords
            
            st.success("Content processed successfully!")

# Query section
if st.session_state.documents:
    st.subheader("Ask Questions")
    
    # Example questions
    with st.expander("Example Questions"):
        st.write("• What is the phone number?")
        st.write("• What is the email address?")
        st.write("• What skills are mentioned?")
        st.write("• What programming languages are listed?")
    
    # User input
    query = st.text_input("Your question:", placeholder="e.g., 'What is the phone number?'")
    
    if query:
        with st.spinner("Searching..."):
            answer = search_and_answer(query, st.session_state.documents)
            
            st.subheader("Answer:")
            st.write(answer)
            
            # Show source documents if needed
            if st.checkbox("Show source documents"):
                st.subheader("Source Documents:")
                for i, doc in enumerate(st.session_state.documents):
                    st.write(f"**Document {i+1}:**")
                    st.text(doc[:500] + "..." if len(doc) > 500 else doc)

# Footer
st.write("---")
st.write("Resume RAG Chatbot - Simple and Functional")