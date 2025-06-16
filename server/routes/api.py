import os, json, uuid, traceback
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER
from utils.file_utils import allowed_file, resize_image, get_image_url
from utils.model_runner import process_image_with_params
from flask import current_app as app

api_bp = Blueprint('api', __name__)

@api_bp.route('/process-image', methods=['POST'])
def process_image_api():
    if 'file' not in request.files or 'metadata' not in request.form:
        return jsonify({'error': '缺少 file 或 metadata 参数'}), 400

    file = request.files['file']
    try:
        metadata = json.loads(request.form['metadata'])
        print(f"接收到文件: {file.filename}")
        print(f"参数: {json.dumps(metadata, indent=2, ensure_ascii=False)}")
        with open('log.json', 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=4, ensure_ascii=False)
    except Exception as e:
        return jsonify({'error': f'metadata 解析失败: {e}'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': '不支持的文件格式'}), 400

    try:
        unique_id = uuid.uuid4().hex
        ext = os.path.splitext(secure_filename(file.filename))[1]
        unique_filename = f"{unique_id}{ext}"
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(input_path)
        resize_image(input_path, max_size=2048)
        output_filename, duration = process_image_with_params(input_path, metadata)

        if not output_filename:
            return jsonify({'error': '处理失败，请查看日志'}), 500

        return jsonify({
            'status': 'success',
            'processing_time': f"{duration:.2f}秒",
            'original_image_url': get_image_url(unique_filename, "uploads"),
            'processed_image_url': get_image_url(output_filename, "processed")
        })
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': f'服务器错误: {e}'}), 500
