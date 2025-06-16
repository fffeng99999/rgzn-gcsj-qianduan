import os

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
BASE_URL = "http://localhost:5000"

BASE_DIR = "D:\\a666\\rgzn_gcsj\\"
MODEL_DIR = os.path.join(BASE_DIR, "SR_UNET2", "output")
SCRIPT_PATH = os.path.join(BASE_DIR, "SR_UNET2", "main.py")
PYTHON_PATH = os.path.join(BASE_DIR, "SR_UNET2", ".venv", "Scripts", "python.exe")

MAX_CONTENT_LENGTH = 10 * 1024 * 1024
