import os
import subprocess
import threading
from flask import Flask

app = Flask(__name__)

REPO_URL = "https://github.com/nari-labs/dia.git"
REPO_DIR = "dia"

# Clone the Dia repository if it doesn't exist
if not os.path.exists(REPO_DIR):
    subprocess.run(["git", "clone", REPO_URL])

# Install the Dia package
subprocess.run(["pip", "install", "-e", "."], cwd=REPO_DIR)

# Function to start the Dia TTS server
def start_dia_server():
    subprocess.run(["python", "app.py"], cwd=REPO_DIR)

# Start the Dia server in a separate thread
threading.Thread(target=start_dia_server).start()

# Flask route to keep the server alive
@app.route('/')
def home():
    return "Nari Labs Dia TTS server is running!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
