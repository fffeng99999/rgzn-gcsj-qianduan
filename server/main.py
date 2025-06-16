import os
from flask import Flask
from flask_cors import CORS
from config import UPLOAD_FOLDER, PROCESSED_FOLDER, MAX_CONTENT_LENGTH
from routes.api import api_bp
from routes.image import image_bp
from routes.test import test_bp

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# 注册蓝图
app.register_blueprint(api_bp)
app.register_blueprint(image_bp)
app.register_blueprint(test_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)



# # 导入标准库
# import os  # 操作文件路径等
# import uuid  # 生成唯一文件名
# import subprocess  # 调用外部 Python 脚本
# import json  # 处理 JSON 数据
# from flask import Flask, request, jsonify, send_file, url_for  # Flask Web框架
# from werkzeug.utils import secure_filename  # 处理上传文件名
# from flask_cors import CORS  # 处理跨域
# import time  # 计时
# from PIL import Image  # 图像处理库 Pillow
#
# # 创建 Flask 应用
# app = Flask(__name__)
# CORS(app)  # 启用跨域支持
#
# # === 配置参数 ===
# UPLOAD_FOLDER = 'uploads'  # 上传文件夹路径
# PROCESSED_FOLDER = 'processed'  # 处理后文件夹路径
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # 允许上传的图片格式
# BASE_URL = "http://localhost:5000"
#
# # 模型目录和脚本路径（需根据你的项目路径配置）
# BASE_DIR = "D:\\a666\\rgzn_gcsj\\"
# MODEL_DIR = BASE_DIR + "\\SR_UNET2\\output"
# SCRIPT_PATH = BASE_DIR + "\\SR_UNET2\\main.py"
# PYTHON_PATH = BASE_DIR + "\\SR_UNET2\\.venv\\Scripts\\python.exe"
#
# # 设置上传文件夹和最大文件大小
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 最大上传 10MB
#
# # 创建上传和处理文件夹（如果不存在则创建）
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(PROCESSED_FOLDER, exist_ok=True)
#
#
# # 判断上传的文件格式是否允许
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#
#
# # 获取图片的访问 URL
# def get_image_url(filename, folder):
#     return url_for('get_image', folder=folder, filename=filename, _external=True)
#
#
# # 用前端参数调用模型推理脚本
# def process_image_with_params(input_path, metadata):
#     try:
#         output_dir = app.config['PROCESSED_FOLDER']
#
#         # 从 metadata 中读取参数，有默认值
#         params = metadata.get('advancedParams', {})
#         scale = params.get('scale', 4)
#         base_channels = params.get('baseChannels', 64)
#         bilinear = params.get('bilinear', False)
#
#         # 获取模型路径
#         model_filename = metadata.get('model', 'unet_best.pth')
#         model_path = os.path.join(MODEL_DIR, model_filename)
#
#         if not os.path.exists(model_path):
#             print(f"错误：模型文件不存在：{model_path}")
#             return None, 0
#
#         # 构建命令行参数调用外部 Python 推理脚本
#         cmd = [
#             PYTHON_PATH, SCRIPT_PATH,
#             "infer",
#             "--checkpoint", model_path,
#             "--lr", input_path,
#             "--output_dir", output_dir,
#             "--lr_scale", str(scale),
#             "--base_channels", str(base_channels),
#         ]
#
#         if bilinear:
#             cmd.append("--bilinear")
#
#         # 打印前端传入的额外参数
#         print(f"前端传入提示词: {metadata.get('prompt', 'N/A')}")
#         print(f"启用的步骤: {metadata.get('steps', {})}")
#         print(f"执行命令: {' '.join(cmd)}")
#
#         # 执行推理脚本并计时
#         start_time = time.time()
#         result = subprocess.run(cmd, capture_output=True, text=True, check=True)
#         duration = time.time() - start_time
#
#         print(f"推理成功（耗时: {duration:.2f}s）")
#         print(f"脚本输出: {result.stdout}")
#
#         # 构建预期输出文件名
#         input_filename_base = os.path.splitext(os.path.basename(input_path))[0]
#         expected_output_filename = f"{input_filename_base}_SR.png"
#         processed_path = os.path.join(output_dir, expected_output_filename)
#
#         if not os.path.exists(processed_path):
#             print(f"错误：找不到输出文件：{processed_path}")
#             return None, 0
#
#         return expected_output_filename, duration
#
#     except subprocess.CalledProcessError as e:
#         print(f"脚本运行出错，返回码: {e.returncode}")
#         print(f"标准错误: {e.stderr}")
#         print(f"标准输出: {e.stdout}")
#         return None, 0
#     except Exception as e:
#         print(f"未知错误: {str(e)}")
#         return None, 0
#
#
# # 图像过大时进行等比例压缩
# def resize_image(image_path, max_size=1024):
#     try:
#         with Image.open(image_path) as img:
#             w, h = img.size
#             if w > max_size or h > max_size:
#                 ratio = min(max_size / w, max_size / h)
#                 new_size = (int(w * ratio), int(h * ratio))
#                 resample_method = Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.ANTIALIAS
#                 img = img.resize(new_size, resample_method)
#                 img.save(image_path)
#                 print(f"已调整图像大小: {image_path} -> {img.size}")
#     except Exception as e:
#         print(f"图像缩放失败: {str(e)}")
#
#
# # 主处理接口
# @app.route('/process-image', methods=['POST'])
# def process_image_api():
#     if 'file' not in request.files:
#         return jsonify({'error': '请求中没有上传文件'}), 400
#     if 'metadata' not in request.form:
#         return jsonify({'error': '请求中没有 metadata 参数'}), 400
#
#     file = request.files['file']
#     metadata_str = request.form['metadata']
#
#     try:
#         metadata = json.loads(metadata_str)
#
#         print("--- 日志记录 ---")
#         print(f"接收到图片文件名: {file.filename}")
#         print(f"接收到前端参数: {json.dumps(metadata, indent=2, ensure_ascii=False)}")
#
#         # 保存日志文件
#         try:
#             with open('log.json', 'w', encoding='utf-8') as f:
#                 json.dump(metadata, f, ensure_ascii=False, indent=4)
#             print("成功保存前端 metadata 到 log.json")
#         except Exception as e:
#             print(f"保存日志文件失败: {e}")
#
#     except json.JSONDecodeError:
#         return jsonify({'error': 'metadata 字段 JSON 格式无效'}), 400
#
#     if file.filename == '' or not allowed_file(file.filename):
#         return jsonify({'error': '文件未选择或格式不支持'}), 400
#
#     try:
#         # 为文件生成唯一名防止覆盖
#         unique_id = uuid.uuid4().hex
#         file_ext = os.path.splitext(secure_filename(file.filename))[1]
#         unique_filename = f"{unique_id}{file_ext}"
#
#         # 保存上传文件
#         input_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
#         file.save(input_path)
#         print(f"已保存上传文件: {input_path}")
#
#         # 调整图片大小
#         resize_image(input_path, max_size=2048)
#
#         # 调用推理函数
#         output_filename, duration = process_image_with_params(input_path, metadata)
#
#         if not output_filename:
#             return jsonify({'error': '服务器处理图片失败，请查看日志'}), 500
#
#         return jsonify({
#             'status': 'success',
#             'processing_time': f"{duration:.2f}秒",
#             'original_image_url': get_image_url(unique_filename, "uploads"),
#             'processed_image_url': get_image_url(output_filename, "processed")
#         })
#
#     except Exception as e:
#         import traceback
#         print(f"/process-image 接口错误: {str(e)}")
#         print(traceback.format_exc())
#         return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500
#
#
# # 提供图片访问接口
# @app.route('/image/<folder>/<filename>')
# def get_image(folder, filename):
#     if folder not in ['uploads', 'processed']:
#         return "无效的文件夹名", 404
#
#     directory = app.config['UPLOAD_FOLDER'] if folder == 'uploads' else app.config['PROCESSED_FOLDER']
#
#     try:
#         return send_file(os.path.join(directory, filename))
#     except FileNotFoundError:
#         return "文件未找到", 404
#
#
# # 测试接口：用于验证服务是否正常运行
# @app.route('/hello', methods=['GET'])
# def testapi():
#     app.logger.info('收到 /hello 请求')
#     return jsonify({"message": "API 服务已启动"})
#
#
# # 启动 Flask 服务
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)
