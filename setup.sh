#!/bin/bash

# Install system dependencies
apt-get update
apt-get install -y python3-pip python3-dev

# Install Python packages
pip3 install -r requirements.txt

# Create necessary directories
mkdir -p .streamlit

# Set up Streamlit configuration
echo "[server]" > .streamlit/config.toml
echo "port = 8501" >> .streamlit/config.toml
echo "address = \"0.0.0.0\"" >> .streamlit/config.toml
echo "baseUrlPath = \"\"" >> .streamlit/config.toml
echo "enableCORS = true" >> .streamlit/config.toml
echo "enableXsrfProtection = false" >> .streamlit/config.toml
echo "" >> .streamlit/config.toml
echo "[browser]" >> .streamlit/config.toml
echo "gatherUsageStats = false" >> .streamlit/config.toml
echo "" >> .streamlit/config.toml
echo "[theme]" >> .streamlit/config.toml
echo "primaryColor = \"#64ffda\"" >> .streamlit/config.toml
echo "backgroundColor = \"#0f0f23\"" >> .streamlit/config.toml
echo "secondaryBackgroundColor = \"#1a1a2e\"" >> .streamlit/config.toml
echo "textColor = \"#e5e5e5\"" >> .streamlit/config.toml

echo "Setup completed successfully!"
