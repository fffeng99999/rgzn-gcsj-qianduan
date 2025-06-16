# config.py

import os

# ===== 核心配置 =====
# 获取项目根目录，使路径更具鲁棒性
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# --- 文件夹路径 ---
UPLOAD_FOLDER = os.path.join(BASE_DIR, './server/uploads')
PROCESSED_FOLDER = os.path.join(BASE_DIR, './server/processed')

# --- 文件设置 ---
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB

# --- 外部脚本和模型路径 (重要: 请根据您的系统更新这些路径) ---
MODEL_DIR = "D:\\a666\\rgzn_gcsj\\SR_UNET2\\output"
SCRIPT_PATH = "D:\\a666\\rgzn_gcsj\\SR_UNET2\\main.py"
PYTHON_PATH = "D:\\a666\\rgzn_gcsj\\SR_UNET2\\.venv\\Scripts\\python.exe"

# --- API 设置 ---
BASE_URL = "http://localhost:5000"