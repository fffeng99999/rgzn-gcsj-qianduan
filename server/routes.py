# routes.py

# import os
# import uuid
# import json
# import traceback
# from flask import Blueprint, request, jsonify, send_file, current_app, url_for
# from werkzeug.utils import secure_filename
# import utils  # 导入我们的工具函数
# import logger  # 导入新的 logger 模块
#
# # 创建一个蓝图对象
# api = Blueprint('api', __name__)
#
# def get_image_url(filename, folder):
#     """获取图像的公共URL。"""
#     # 'api.get_image' 引用了蓝图名称'api'和函数名'get_image'
#     return url_for('api.get_image', folder=folder, filename=filename, _external=True)
#
# @api.route('/process-image', methods=['POST'])
# def process_image_api():
#     """处理图像和元数据的API端点。"""
#     if 'file' not in request.files or 'metadata' not in request.form:
#         return jsonify({'error': '请求必须包含文件和元数据'}), 400
#
#     file = request.files['file']
#     metadata_str = request.form['metadata']
#
#     try:
#         metadata = json.loads(metadata_str)
#
#         # 调用专用的日志记录函数
#         logger.log_request_data(file.filename, metadata)
#
#     except json.JSONDecodeError:
#         return jsonify({'error': '元数据中的JSON格式无效'}), 400
#
#     if file.filename == '' or not utils.allowed_file(file.filename):
#         return jsonify({'error': '未选择文件或文件类型不允许'}), 400
#
#     try:
#         # 记录接收到的数据
#         print(f"接收到元数据: {json.dumps(metadata, indent=2, ensure_ascii=False)}")
#
#         # 保存并处理文件
#         unique_id = uuid.uuid4().hex
#         file_ext = os.path.splitext(secure_filename(file.filename))[1]
#         unique_filename = f"{unique_id}{file_ext}"
#         input_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
#         file.save(input_path)
#         print(f"上传文件已保存至: {input_path}")
#
#         utils.resize_image(input_path, max_size=2048)
#         output_filename, duration = utils.process_image_with_params(input_path, metadata)
#
#         if not output_filename:
#             return jsonify({'error': '服务器图像处理失败，请检查日志。'}), 500
#
#         return jsonify({
#             'status': 'success',
#             'processing_time': f"{duration:.2f}秒",
#             'original_image_url': get_image_url(unique_filename, "uploads"),
#             'processed_image_url': get_image_url(output_filename, "processed")
#         })
#
#     except Exception as e:
#         print(f"端点 /process-image 发生错误: {str(e)}")
#         print(traceback.format_exc())
#         return jsonify({'error': f'发生内部服务器错误: {str(e)}'}), 500
#
# @api.route('/image/<folder>/<filename>')
# def get_image(folder, filename):
#     """从 'uploads' 或 'processed' 目录提供图像。"""
#     if folder not in ['uploads', 'processed']:
#         return "指定的文件夹无效", 404
#
#     directory = current_app.config['UPLOAD_FOLDER'] if folder == 'uploads' else current_app.config['PROCESSED_FOLDER']
#     try:
#         return send_file(os.path.join(directory, filename))
#     except FileNotFoundError:
#         return "文件未找到", 404
#
# @api.route('/hello', methods=['GET'])
# def test_api():
#     """一个简单的测试端点，用于确认API正在运行。"""
#     current_app.logger.info('收到 /hello 请求')
#     return jsonify({"message": "API服务正在运行"})
#
#


# server/routes.py

import os
import uuid
import json
import traceback
from flask import Blueprint, request, jsonify, send_file, current_app, url_for
from werkzeug.utils import secure_filename
import utils  # 导入我们的工具函数
import logger  # 导入新的 logger 模块

# 创建一个蓝图对象 (从 'api' 修改为 'main')
main = Blueprint('main', __name__)

def get_image_url(filename, folder):
    """获取图像的公共URL。"""
    # 'main.get_image' 引用了蓝图名称'main'和函数名'get_image'
    return url_for('main.get_image', folder=folder, filename=filename, _external=True)

@main.route('/process-image', methods=['POST'])
def process_image_api():
    """处理图像和元数据的API端点。"""
    if 'file' not in request.files or 'metadata' not in request.form:
        return jsonify({'error': '请求必须包含文件和元数据'}), 400

    file = request.files['file']
    metadata_str = request.form['metadata']

    try:
        metadata = json.loads(metadata_str)

        # 调用专用的日志记录函数
        logger.log_request_data(file.filename, metadata)

    except json.JSONDecodeError:
        return jsonify({'error': '元数据中的JSON格式无效'}), 400

    if file.filename == '' or not utils.allowed_file(file.filename):
        return jsonify({'error': '未选择文件或文件类型不允许'}), 400

    try:
        # 记录接收到的数据
        print(f"接收到元数据: {json.dumps(metadata, indent=2, ensure_ascii=False)}")

        # 从 metadata 中提取 parameters
        # 确保你的前端在发送请求时，将模型预设参数作为 `parameters` 字段包含在 `metadata` 中
        parameters = metadata.get('parameters', {})
        print(f"接收到模型参数: {json.dumps(parameters, indent=2, ensure_ascii=False)}")


        # 保存并处理文件
        unique_id = uuid.uuid4().hex
        file_ext = os.path.splitext(secure_filename(file.filename))[1]
        unique_filename = f"{unique_id}{file_ext}"
        input_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(input_path)
        print(f"上传文件已保存至: {input_path}")

        utils.resize_image(input_path, max_size=2048)
        # 将 parameters 传递给处理函数
        output_filename, duration = utils.process_image_with_params(input_path, parameters)

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

@main.route('/image/<folder>/<filename>')
def get_image(folder, filename):
    """从 'uploads' 或 'processed' 目录提供图像。"""
    if folder not in ['uploads', 'processed']:
        return "指定的文件夹无效", 404

    # 使用 current_app.config 来获取正确的目录
    directory = current_app.config['UPLOAD_FOLDER'] if folder == 'uploads' else current_app.config['PROCESSED_FOLDER']
    try:
        return send_file(os.path.join(directory, filename))
    except FileNotFoundError:
        return "文件未找到", 404

@main.route('/hello', methods=['GET'])
def test_api():
    """一个简单的测试端点，用于确认API正在运行。"""
    current_app.logger.info('收到 /hello 请求')
    return jsonify({"message": "API服务正在运行"})


# --- NEW ROUTE: Fetch Model Parameters ---
@main.route('/model-parameters/<model_name>', methods=['GET'])
def get_model_parameters(model_name):
    """根据模型名称获取预制的模型参数。"""
    try:
        # 清理模型名称以防止目录遍历攻击
        secure_model_name = secure_filename(model_name)

        # 定义到 md_parameters 目录的路径
        # current_app.root_path 指向 Flask 应用的根目录 (通常是 server 目录)
        data_dir = os.path.join(current_app.root_path, 'data', 'md_parameters')

        # 假设模型名称（例如 'unet_best'）对应文件名为 'unet_best.json'
        file_path = os.path.join(data_dir, f"{secure_model_name}.json")

        if not os.path.exists(file_path):
            logger.warning(f"模型参数文件未找到: {file_path}")
            return jsonify({"error": "Model parameters not found"}), 404

        with open(file_path, 'r', encoding='utf-8') as f:
            parameters = json.load(f)

        logger.info(f"成功加载模型参数: {model_name}")
        return jsonify(parameters), 200

    except Exception as e:
        logger.error(f"获取模型参数时发生错误 {model_name}: {e}")
        print(traceback.format_exc()) # 打印完整的堆栈跟踪以便调试
        return jsonify({"error": "Internal server error"}), 500

# --- NEW ROUTE: List Available Models ---
@main.route('/models', methods=['GET'])
def list_models():
    """列出所有可用的模型名称。"""
    try:
        data_dir = os.path.join(current_app.root_path, 'data', 'md_parameters')
        if not os.path.exists(data_dir):
            # 如果目录不存在，返回空列表而不是错误
            logger.warning(f"模型参数目录不存在: {data_dir}")
            return jsonify({"models": []}), 200

        model_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
        # 提取模型名称（不带 .json 扩展名）
        models = [os.path.splitext(f)[0] for f in model_files]
        logger.info(f"列出可用模型: {models}")
        return jsonify({"models": models}), 200
    except Exception as e:
        logger.error(f"列出模型时发生错误: {e}")
        print(traceback.format_exc()) # 打印完整的堆栈跟踪以便调试
        return jsonify({"error": "Internal server error"}), 500