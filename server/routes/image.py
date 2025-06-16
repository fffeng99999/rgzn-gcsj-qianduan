import os
from flask import Blueprint, send_file, current_app as app

image_bp = Blueprint('image', __name__)

@image_bp.route('/image/<folder>/<filename>')
def get_image(folder, filename):
    if folder not in ['uploads', 'processed']:
        return "无效的文件夹名", 404

    directory = app.config['UPLOAD_FOLDER'] if folder == 'uploads' else app.config['PROCESSED_FOLDER']
    try:
        return send_file(os.path.join(directory, filename))
    except FileNotFoundError:
        return "文件未找到", 404
