# 🤖 Resume RAG Chatbot

An AI-powered resume analysis and candidate screening application built with Streamlit. Features a ChatGPT-5 inspired interface with intelligent text processing capabilities.

## ✨ Features

### 🎯 Core Functionality
- **� Text input support** - Paste resume content directly or upload text files
- **🔍 Smart keyword search** with relevance scoring
- **💬 Natural language queries** with precise pattern-matching answers
- **📱 Responsive design** - Works perfectly on all devices
- **⚡ Fast processing** with optimized search algorithms

### 🎨 Modern Interface
- **ChatGPT-5 inspired design** with dark theme
- **Glassmorphism effects** and smooth animations
- **Clean, professional layout** optimized for productivity
- **Intuitive user experience** with helpful examples

### 🔍 Smart Search Capabilities
- Extract contact information (phone, email)
- Identify technical skills and programming languages
- Find experience levels and years of work
- Search for specific qualifications and keywords

## 🚀 Quick Start

### 🌐 Online Access
**Live Demo**: [https://resume-filter-chatbot.streamlit.app/](https://resume-filter-chatbot.streamlit.app/)

### Local Development
```bash
# Clone the repository
git clone https://github.com/panneerit89/streamlit-resume-rag.git
cd streamlit-resume-rag

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run rag_chatbot.py
```

### 🚀 Deploy Your Own

#### Streamlit Cloud Deployment (Recommended)
1. **Fork** this repository to your GitHub account
2. **Go to** [share.streamlit.io](https://share.streamlit.io)
3. **Sign in** with your GitHub account
4. **Click** "New app"
5. **Repository**: `your-username/streamlit-resume-rag`
6. **Main file path**: `rag_chatbot.py`
7. **Click** "Deploy!"
## 📖 How to Use

1. **Access the app** at [resume-filter-chatbot.streamlit.app](https://resume-filter-chatbot.streamlit.app/)

2. **Upload content** using one of these methods:
   - **Paste text**: Copy resume content directly into the text area
   - **Upload files**: Upload .txt or .md files containing resume text

3. **Ask questions** about the candidates:
   - "What is the phone number?"
   - "What skills are mentioned?"
   - "How many years of experience?"
   - "What is the email address?"

## 🎯 Example Queries

### Contact Information
- "What is the phone number?"
- "Show me the email address"
- "Find contact details"

### Skills & Experience
- "What programming languages are mentioned?"
- "List the technical skills"
- "How many years of Python experience?"
- "What technologies does the candidate know?"

### General Information
- "What is the candidate's name?"
- "Find project management experience"
- "Show me the work history"

## 🛠️ Technical Details

### Dependencies
```
streamlit        # Web application framework
numpy           # Numerical computations
pandas          # Data manipulation
requests        # HTTP requests
```

### Architecture
The application uses a lightweight, dependency-free approach:
- **Text Processing**: Pure Python regex and string operations
- **Keyword Extraction**: Custom algorithm with stop word removal
- **Search Strategy**: TF-IDF-like relevance scoring
- **Pattern Matching**: Regex patterns for precise information extraction
- **No ML Dependencies**: Fast, reliable processing without heavy libraries

### Key Features
- **Zero ML Dependencies**: No complex machine learning libraries
- **Fast Performance**: Instant responses with simple algorithms
- **Reliable Results**: Regex patterns ensure accurate extraction
- **Lightweight**: Minimal dependencies for quick deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🚀 Deployment Status

- **Live Demo**: [https://resume-filter-chatbot.streamlit.app/](https://resume-filter-chatbot.streamlit.app/)
- **Platform**: Streamlit Cloud
- **Repository**: [GitHub](https://github.com/panneerit89/streamlit-resume-rag)
- **Status**: ✅ Active

## 📞 Support

For questions or support, please open an issue on GitHub or contact the maintainer.

---

**Built with ❤️ using Streamlit and Python**
- **Experience**: Years of experience, work history
- **General Information**: Education, certifications, projects
