# utils.py

import os
import subprocess
import time
from PIL import Image
import config  # 导入我们的配置文件

def allowed_file(filename):
    """检查文件扩展名是否在允许的列表中。"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

def resize_image(image_path, max_size=1024):
    """如果图像尺寸过大，则进行缩放。"""
    try:
        with Image.open(image_path) as img:
            w, h = img.size
            if w > max_size or h > max_size:
                ratio = min(max_size / w, max_size / h)
                new_size = (int(w * ratio), int(h * ratio))
                resample_method = Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.ANTIALIAS
                img = img.resize(new_size, resample_method)
                img.save(image_path)
                print(f"图像已缩放: {image_path} to {img.size}")
    except Exception as e:
        print(f"缩放图像失败: {str(e)}")

def process_image_with_params(input_path, metadata):
    """使用从前端元数据中获取的参数调用推理脚本。"""
    try:
        params = metadata.get('advancedParams', {})
        scale = params.get('scale', 4)
        base_channels = params.get('baseChannels', 64)
        bilinear = params.get('bilinear', False)
        model_filename = metadata.get('model', 'unet_best.pth')
        model_path = os.path.join(config.MODEL_DIR, model_filename)

        if not os.path.exists(model_path):
            print(f"错误: 模型文件未找到于 {model_path}")
            return None, 0

        # 动态构建命令
        cmd = [
            config.PYTHON_PATH, config.SCRIPT_PATH,
            "infer",
            "--checkpoint", model_path,
            "--lr", input_path,
            "--output_dir", config.PROCESSED_FOLDER,
            "--lr_scale", str(scale),
            "--base_channels", str(base_channels),
        ]
        if bilinear:
            cmd.append("--bilinear")

        print(f"执行命令: {' '.join(cmd)}")
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        duration = time.time() - start_time
        print(f"推理成功 (耗时: {duration:.2f}s)")
        print(f"脚本标准输出: {result.stdout}")

        # 查找生成的输出文件
        input_filename_base = os.path.splitext(os.path.basename(input_path))[0]
        expected_output_filename = f"{input_filename_base}_SR.png"
        processed_path = os.path.join(config.PROCESSED_FOLDER, expected_output_filename)

        if not os.path.exists(processed_path):
            print(f"错误: 预期的输出文件未找到于 {processed_path}")
            return None, 0

        return expected_output_filename, duration

    except subprocess.CalledProcessError as e:
        print(f"脚本执行出错。返回码: {e.returncode}")
        print(f"标准错误: {e.stderr}")
        print(f"标准输出: {e.stdout}")
        return None, 0
    except Exception as e:
        print(f"process_image_with_params 中发生意外错误: {str(e)}")
        return None, 0