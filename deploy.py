#!/usr/bin/env python3

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def setup_streamlit_config():
    """Setup Streamlit configuration for deployment"""
    os.makedirs(".streamlit", exist_ok=True)
    
    config_content = """[server]
port = 8501
address = "0.0.0.0"
baseUrlPath = ""
enableCORS = true
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#64ffda"
backgroundColor = "#0f0f23"
secondaryBackgroundColor = "#1a1a2e"
textColor = "#e5e5e5"
"""
    
    with open(".streamlit/config.toml", "w") as f:
        f.write(config_content)

def main():
    """Main deployment setup function"""
    print("Setting up Resume RAG Chatbot for deployment...")
    
    try:
        install_requirements()
        print("✅ Requirements installed successfully")
        
        setup_streamlit_config()
        print("✅ Streamlit configuration created")
        
        print("🚀 Setup completed! Ready for deployment.")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
