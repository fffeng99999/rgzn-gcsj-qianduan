# fffeng99999/rgzn-gcsj-qianduan/rgzn-gcsj-qianduan-1380fd747a3f68c1ae28cea72052197a6290bc74/server/routes/api.py
import os
import uuid
import json
import traceback
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from server.utils.file_utils import allowed_file, get_image_url, resize_image
from server.utils.model_runner import run_inference

api_bp = Blueprint('api', __name__)

@api_bp.route('/process-image', methods=['POST'])
def process_image_api():
    if 'file' not in request.files:
        return jsonify({'error': '请求中没有上传文件 (file part is missing)'}), 400
    if 'metadata' not in request.form:
        return jsonify({'error': '请求中没有元数据 (metadata part is missing)'}), 400

    file = request.files['file']
    metadata_str = request.form['metadata']

    try:
        metadata = json.loads(metadata_str)
        print("接收到文件:", file.filename)
        print("参数:", json.dumps(metadata, indent=2, ensure_ascii=False))
    except json.JSONDecodeError:
        return jsonify({'error': 'Metadata JSON 格式无效'}), 400

    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': '文件未选择或文件格式不支持'}), 400

    try:
        # 生成唯一文件名
        unique_id = uuid.uuid4().hex
        file_ext = os.path.splitext(secure_filename(file.filename))[1]
        unique_filename = f"{unique_id}{file_ext}"

        # 保存上传文件
        upload_folder = current_app.config['UPLOAD_FOLDER']
        input_path = os.path.join(upload_folder, unique_filename)
        file.save(input_path)
        print(f"文件已保存到: {input_path}")

        # [新增] 调用图片缩放功能，与旧代码逻辑保持一致
        resize_image(input_path)

        # [修改] 调用推理函数，并传入 app config
        output_filename, duration = run_inference(current_app.config, input_path, metadata)

        if not output_filename:
            return jsonify({'error': '服务器处理图片失败，请检查后台日志'}), 500

        # 使用修正后的 get_image_url 生成链接
        original_url = get_image_url(unique_filename, "uploads")
        processed_url = get_image_url(output_filename, "processed")

        return jsonify({
            'status': 'success',
            'processing_time': f"{duration:.2f}秒",
            'original_image_url': original_url,
            'processed_image_url': processed_url,
        })

    except Exception as e:
        print(f"处理 /process-image 请求时发生严重错误: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'服务器内部发生严重错误: {str(e)}'}), 500