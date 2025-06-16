import os
import time
import subprocess
from config import MODEL_DIR, PYTHON_PATH, SCRIPT_PATH
from flask import current_app as app

def process_image_with_params(input_path, metadata):
    try:
        output_dir = app.config['PROCESSED_FOLDER']
        params = metadata.get('advancedParams', {})
        scale = params.get('scale', 4)
        base_channels = params.get('baseChannels', 64)
        bilinear = params.get('bilinear', False)

        model_filename = metadata.get('model', 'unet_best.pth')
        model_path = os.path.join(MODEL_DIR, model_filename)

        if not os.path.exists(model_path):
            print(f"模型不存在：{model_path}")
            return None, 0

        cmd = [
            PYTHON_PATH, SCRIPT_PATH,
            "infer",
            "--checkpoint", model_path,
            "--lr", input_path,
            "--output_dir", output_dir,
            "--lr_scale", str(scale),
            "--base_channels", str(base_channels),
        ]
        if bilinear:
            cmd.append("--bilinear")

        print(f"前端提示词: {metadata.get('prompt', 'N/A')}")
        print(f"启用步骤: {metadata.get('steps', {})}")
        print(f"执行命令: {' '.join(cmd)}")

        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        duration = time.time() - start_time

        print(f"推理成功（耗时: {duration:.2f}s）")
        print(f"输出: {result.stdout}")

        input_filename_base = os.path.splitext(os.path.basename(input_path))[0]
        expected_output_filename = f"{input_filename_base}_SR.png"
        processed_path = os.path.join(output_dir, expected_output_filename)

        if not os.path.exists(processed_path):
            print(f"输出文件缺失：{processed_path}")
            return None, 0

        return expected_output_filename, duration

    except subprocess.CalledProcessError as e:
        print(f"脚本错误: {e.stderr}")
        return None, 0
    except Exception as e:
        print(f"未知错误: {e}")
        return None, 0
