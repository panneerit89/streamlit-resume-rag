const { spawn } = require('child_process');

exports.handler = async (event, context) => {
  return new Promise((resolve, reject) => {
    const streamlit = spawn('streamlit', ['run', 'rag_chatbot.py', '--server.port=8501'], {
      cwd: process.cwd(),
      stdio: 'pipe'
    });

    streamlit.on('close', (code) => {
      resolve({
        statusCode: 200,
        body: JSON.stringify({
          message: 'Streamlit app is running',
          code: code
        })
      });
    });

    streamlit.on('error', (error) => {
      reject({
        statusCode: 500,
        body: JSON.stringify({
          error: error.message
        })
      });
    });
  });
};
