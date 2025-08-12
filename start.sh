#!/bin/bash

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create Streamlit config directory
mkdir -p ~/.streamlit

# Create Streamlit config
cat > ~/.streamlit/config.toml << EOF
[server]
port = 8501
address = "0.0.0.0"
baseUrlPath = ""
enableCORS = true
enableXsrfProtection = false
headless = true

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#64ffda"
backgroundColor = "#0f0f23"
secondaryBackgroundColor = "#1a1a2e"
textColor = "#e5e5e5"
EOF

echo "Starting Streamlit app..."
streamlit run rag_chatbot.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true
