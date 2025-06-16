import os
from werkzeug.utils import secure_filename
from PIL import Image
from flask import url_for
from config import ALLOWED_EXTENSIONS

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_image_url(filename, folder):
    return url_for('get_image', folder=folder, filename=filename, _external=True)

def resize_image(image_path, max_size=1024):
    try:
        with Image.open(image_path) as img:
            w, h = img.size
            if w > max_size or h > max_size:
                ratio = min(max_size / w, max_size / h)
                new_size = (int(w * ratio), int(h * ratio))
                resample = Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.ANTIALIAS
                img = img.resize(new_size, resample)
                img.save(image_path)
                print(f"已调整图像大小: {image_path} -> {img.size}")
    except Exception as e:
        print(f"图像缩放失败: {str(e)}")
