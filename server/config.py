# fffeng99999/rgzn-gcsj-qianduan/rgzn-gcsj-qianduan-1380fd747a3f68c1ae28cea72052197a6290bc74/server/config.py
import os

# === 核心配置 ===
# 请根据你的项目路径修改这里的 BASE_DIR
BASE_DIR = "D:\\a666\\rgzn_gcsj\\SR_UNET2"

# 文件夹路径
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
PROCESSED_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'processed')

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 模型和脚本路径
MODEL_DIR = os.path.join(BASE_DIR, "output")
SCRIPT_PATH = os.path.join(BASE_DIR, "main.py")
PYTHON_PATH = os.path.join(BASE_DIR, ".venv", "Scripts", "python.exe")


def configure_app(app):
    """为 Flask app 应用配置"""
    # 设置上传文件夹和处理后文件夹
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 最大上传 16MB

    # 将其他常量也存入 config，方便全局调用
    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
    app.config['MODEL_DIR'] = MODEL_DIR
    app.config['SCRIPT_PATH'] = SCRIPT_PATH
    app.config['PYTHON_PATH'] = PYTHON_PATH

    # 确保文件夹存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

