# fffeng99999/rgzn-gcsj-qianduan/rgzn-gcsj-qianduan-1380fd747a3f68c1ae28cea72052197a6290bc74/server/utils/file_utils.py
import os
from flask import url_for, current_app
from PIL import Image

def allowed_file(filename):
    """检查文件扩展名是否在允许的范围内"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def get_image_url(filename, folder):
    """
    为指定文件夹中的文件生成可访问的 URL。
    修正了 url_for 的端点，从 'get_image' 改为 'image.get_image'。
    """
    if not filename:
        return None
    # 关键修正：使用 'image.get_image' 来引用 image 蓝图中的 get_image 函数
    return url_for('image.get_image', folder=folder, filename=filename, _external=True)

def resize_image(image_path, max_size=2048):
    """
    如果图像尺寸过大，则进行等比例缩放。
    这是从旧代码迁移过来的功能。
    """
    try:
        with Image.open(image_path) as img:
            w, h = img.size
            if w > max_size or h > max_size:
                ratio = min(max_size / w, max_size / h)
                new_size = (int(w * ratio), int(h * ratio))
                # Pillow 9.0.0 后 resample 方法有变化
                resample_method = Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.ANTIALIAS
                img = img.resize(new_size, resample_method)
                img.save(image_path)
                print(f"图像尺寸已调整: {image_path} -> {img.size}")
    except Exception as e:
        print(f"图像缩放失败: {str(e)}")