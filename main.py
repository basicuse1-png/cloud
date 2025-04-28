import os
import subprocess
import threading
from flask import Flask

app = Flask(__name__)

# Clone the Nari Labs Dia TTS repository
REPO_URL = "https://github.com/nari-labs/dia.git"
REPO_DIR = "dia"

if not os.path.exists(REPO_DIR):
    print("Cloning the Dia repository...")
    subprocess.run(["git", "clone", REPO_URL])

# Install requirements
print("Installing Dia requirements...")
subprocess.run(["pip", "install", "-e", "."], cwd=REPO_DIR)

# Function to start the Dia TTS server
def start_dia_server():
    print("Starting the Dia TTS server...")
    subprocess.run(["python", "app.py"], cwd=REPO_DIR)

# Start the Dia server in a separate thread
threading.Thread(target=start_dia_server).start()

# Flask route to keep the server alive
@app.route('/')
def home():
    return "Nari Labs Dia TTS server is running!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
