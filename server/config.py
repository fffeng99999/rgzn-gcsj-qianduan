# config.py

import os

# ===== 核心配置 =====
# 获取项目根目录，使路径更具鲁棒性
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# --- 文件夹路径 ---
UPLOAD_FOLDER = os.path.join(BASE_DIR, './data/uploads')
PROCESSED_FOLDER = os.path.join(BASE_DIR, './data/processed')

# --- 文件设置 ---
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB

# --- 外部脚本和模型路径 (重要: 请根据您的系统更新这些路径) ---0
BASE_MODEL_DIR = "D:\\a666\\rgzn_gcsj\\"
MODEL_DIR = BASE_MODEL_DIR + "SR_UNET2\\output"
SCRIPT_PATH = BASE_MODEL_DIR + "\\SR_UNET2\\main.py"
PYTHON_PATH = BASE_MODEL_DIR + "\\SR_UNET2\\.venv\\Scripts\\python.exe"

# --- API 设置 ---
BASE_URL = "http://localhost:5000"

# 日志目录
LOG_FILE_PATH = os.path.join(BASE_DIR, 'log.json')

USE_REAL_DATA = False