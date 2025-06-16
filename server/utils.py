# utils.py

# 脚本处理
import os
import subprocess
import time
import json
from PIL import Image
from werkzeug.utils import secure_filename
import config  # 导入我们的配置文件

def allowed_file(filename):
    """检查文件扩展名是否在允许的列表中。"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

def resize_image(image_path, max_size=2048):
    """如果图像尺寸过大，则进行缩放。"""
    try:
        with Image.open(image_path) as img:
            w, h = img.size
            if w > max_size or h > max_size:
                ratio = min(max_size / w, max_size / h)
                new_size = (int(w * ratio), int(h * ratio))
                resample_method = Image.Resampling.LANCZOS if hasattr(Image.Resampling, 'LANCZOS') else Image.ANTIALIAS
                img = img.resize(new_size, resample_method)
                img.save(image_path)
                print(f"图像已缩放: {image_path} to {img.size}")
    except Exception as e:
        print(f"缩放图像失败: {str(e)}")

def process_image_with_params(input_path, metadata):
    """
    根据元数据中的模型名称，调用对应的专用模型启动器脚本。
    """
    try:
        # 1. 从元数据中安全地获取模型名称
        model_name = metadata.get('model')
        if not model_name:
            print("错误: 元数据中未指定 'model'。")
            return None, 0

        # 2. 清理模型名称以防范路径遍历攻击，并构建启动器脚本的路径
        secure_model_name = secure_filename(model_name)
        runner_script_name = f"{secure_model_name}.py"
        runner_script_path = os.path.join(config.BASE_DIR, 'model_runners', runner_script_name)

        if not os.path.exists(runner_script_path):
            print(f"错误: 找不到模型启动器脚本: {runner_script_path}")
            return None, 0

        # 3. 准备调用启动器脚本的命令
        # 我们将所有参数序列化为JSON字符串，传递给启动器，实现最大灵活性
        params_json = json.dumps(metadata)
        cmd = [
            config.PYTHON_PATH,
            runner_script_path,
            "--input", input_path,
            "--output_dir", config.PROCESSED_FOLDER,
            "--params", params_json
        ]

        print(f"正在执行启动器脚本: {' '.join(cmd)}")
        start_time = time.time()

        # 4. 执行子进程，并捕获其输出
        result = subprocess.run(
            cmd,
            capture_output=True,  # 捕获 stdout 和 stderr
            text=True,            # 以文本模式处理输出
            check=True            # 如果脚本返回非零退出码，则抛出异常
        )
        duration = time.time() - start_time
        print(f"启动器脚本执行完毕 (耗时: {duration:.2f}s)")
        # 打印启动器的日志/错误信息，便于调试
        if result.stderr:
            print(f"来自启动器脚本的日志/错误信息:\n---_--_\n{result.stderr.strip()}\n---_--_")

        # 5. 从启动器的标准输出中解析出最终的文件名
        output_filename = None
        for line in result.stdout.splitlines():
            if line.startswith("OUTPUT_FILENAME:"):
                output_filename = line.split(":", 1)[1].strip()
                break

        if not output_filename:
            print("错误: 未能从启动器脚本的输出中找到 'OUTPUT_FILENAME:'。")
            print(f"启动器脚本的标准输出: {result.stdout}")
            return None, 0

        print(f"启动器脚本报告的输出文件为: {output_filename}")
        return output_filename, duration

    except subprocess.CalledProcessError as e:
        print(f"启动器脚本执行失败。返回码: {e.returncode}")
        print(f"标准输出: {e.stdout}")
        print(f"标准错误: {e.stderr}")
        return None, 0
    except Exception as e:
        print(f"在 process_image_with_params 中发生意外错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, 0



# 模型处理

# import os
# import subprocess
# import time
# from PIL import Image
# import config  # 导入我们的配置文件
#
# def allowed_file(filename):
#     """检查文件扩展名是否在允许的列表中。"""
#     return '.' in filename and \
#         filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS
#
# def resize_image(image_path, max_size=1024):
#     """如果图像尺寸过大，则进行缩放。"""
#     try:
#         with Image.open(image_path) as img:
#             w, h = img.size
#             if w > max_size or h > max_size:
#                 ratio = min(max_size / w, max_size / h)
#                 new_size = (int(w * ratio), int(h * ratio))
#                 resample_method = Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.ANTIALIAS
#                 img = img.resize(new_size, resample_method)
#                 img.save(image_path)
#                 print(f"图像已缩放: {image_path} to {img.size}")
#     except Exception as e:
#         print(f"缩放图像失败: {str(e)}")
#
# def process_image_with_params(input_path, metadata):
#     """使用从前端元数据中获取的参数调用推理脚本。"""
#     try:
#         params = metadata.get('advancedParams', {})
#         scale = params.get('scale', 4)
#         base_channels = params.get('baseChannels', 64)
#         bilinear = params.get('bilinear', False)
#         model_filename = metadata.get('model', 'unet_best.pth')
#         model_path = os.path.join(config.MODEL_DIR, model_filename)
#
#         if not os.path.exists(model_path):
#             print(f"错误: 模型文件未找到于 {model_path}")
#             return None, 0
#
#         # 动态构建命令
#         cmd = [
#             config.PYTHON_PATH, config.SCRIPT_PATH,
#             "infer",
#             "--checkpoint", model_path,
#             "--lr", input_path,
#             "--output_dir", config.PROCESSED_FOLDER,
#             "--lr_scale", str(scale),
#             "--base_channels", str(base_channels),
#         ]
#         if bilinear:
#             cmd.append("--bilinear")
#
#         print(f"执行命令: {' '.join(cmd)}")
#         start_time = time.time()
#         result = subprocess.run(cmd, capture_output=True, text=True, check=True)
#         duration = time.time() - start_time
#         print(f"推理成功 (耗时: {duration:.2f}s)")
#         print(f"脚本标准输出: {result.stdout}")
#
#         # 查找生成的输出文件
#         input_filename_base = os.path.splitext(os.path.basename(input_path))[0]
#         expected_output_filename = f"{input_filename_base}_SR.png"
#         processed_path = os.path.join(config.PROCESSED_FOLDER, expected_output_filename)
#
#         if not os.path.exists(processed_path):
#             print(f"错误: 预期的输出文件未找到于 {processed_path}")
#             return None, 0
#
#         return expected_output_filename, duration
#
#     except subprocess.CalledProcessError as e:
#         print(f"脚本执行出错。返回码: {e.returncode}")
#         print(f"标准错误: {e.stderr}")
#         print(f"标准输出: {e.stdout}")
#         return None, 0
#     except Exception as e:
#         print(f"process_image_with_params 中发生意外错误: {str(e)}")
#         return None, 0