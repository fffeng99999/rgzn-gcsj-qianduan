# routes.py

import os
import uuid
import json
import traceback
from flask import Blueprint, request, jsonify, send_file, current_app, url_for
from werkzeug.utils import secure_filename
import utils  # 导入我们的工具函数

# 创建一个蓝图对象
api = Blueprint('api', __name__)

def get_image_url(filename, folder):
    """获取图像的公共URL。"""
    # 'api.get_image' 引用了蓝图名称'api'和函数名'get_image'
    return url_for('api.get_image', folder=folder, filename=filename, _external=True)

@api.route('/process-image', methods=['POST'])
def process_image_api():
    """处理图像和元数据的API端点。"""
    if 'file' not in request.files or 'metadata' not in request.form:
        return jsonify({'error': '请求必须包含文件和元数据'}), 400

    file = request.files['file']
    metadata_str = request.form['metadata']

    try:
        metadata = json.loads(metadata_str)
    except json.JSONDecodeError:
        return jsonify({'error': '元数据中的JSON格式无效'}), 400

    if file.filename == '' or not utils.allowed_file(file.filename):
        return jsonify({'error': '未选择文件或文件类型不允许'}), 400

    try:
        # 记录接收到的数据
        print(f"接收到元数据: {json.dumps(metadata, indent=2, ensure_ascii=False)}")

        # 保存并处理文件
        unique_id = uuid.uuid4().hex
        file_ext = os.path.splitext(secure_filename(file.filename))[1]
        unique_filename = f"{unique_id}{file_ext}"
        input_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(input_path)
        print(f"上传文件已保存至: {input_path}")

        utils.resize_image(input_path, max_size=2048)
        output_filename, duration = utils.process_image_with_params(input_path, metadata)

        if not output_filename:
            return jsonify({'error': '服务器图像处理失败，请检查日志。'}), 500

        return jsonify({
            'status': 'success',
            'processing_time': f"{duration:.2f}秒",
            'original_image_url': get_image_url(unique_filename, "uploads"),
            'processed_image_url': get_image_url(output_filename, "processed")
        })

    except Exception as e:
        print(f"端点 /process-image 发生错误: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'发生内部服务器错误: {str(e)}'}), 500

@api.route('/image/<folder>/<filename>')
def get_image(folder, filename):
    """从 'uploads' 或 'processed' 目录提供图像。"""
    if folder not in ['uploads', 'processed']:
        return "指定的文件夹无效", 404

    directory = current_app.config['UPLOAD_FOLDER'] if folder == 'uploads' else current_app.config['PROCESSED_FOLDER']
    try:
        return send_file(os.path.join(directory, filename))
    except FileNotFoundError:
        return "文件未找到", 404

@api.route('/hello', methods=['GET'])
def test_api():
    """一个简单的测试端点，用于确认API正在运行。"""
    current_app.logger.info('收到 /hello 请求')
    return jsonify({"message": "API服务正在运行"})