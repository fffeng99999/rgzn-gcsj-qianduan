# app.py

import os
from flask import Flask
from flask_cors import CORS
import config       # 导入配置
from routes import api  # 导入蓝图

def create_app():
    """创建并配置Flask应用。"""
    app = Flask(__name__)

    # --- 从对象加载配置 ---
    app.config.from_object(config)

    # --- 初始化扩展 ---
    CORS(app)

    # --- 创建必要的目录 ---
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

    # --- 注册蓝图 ---
    app.register_blueprint(api)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)