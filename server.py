from api.endpoints import *
from flask import Flask
from flask_cors import CORS
import os
import sys
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)

# Add parent directory to path (for util)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Add api directory to path
sys.path.append(os.path.join(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))), 'api'))


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 10  # 25 MB


@app.route("/")
def hello_world():
    return "hello world!"


GenerateFlashcardsEndpoint(app)
ImproveParagraphEndpoint(app)
HTMLToPDFEndpoint(app)
HTMLToDocxEndpoint(app)
# app = app.wsgi_app
# wsgi_app = app
if __name__ == "__main__":
    app.run(debug=True, port=5000)
