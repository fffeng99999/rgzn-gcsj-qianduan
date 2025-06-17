# /server/runners/unet_best.py

import argparse
import json
import os
import subprocess
import sys
import time

# 将父目录 (server) 添加到系统路径中，以便能够导入 config 模块
# 这使得 runner 脚本可以独立运行，同时又能访问共享的配置
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

def run_unet_model(input_path, output_dir, params_json):
    """
    运行 UNET 模型推理的核心逻辑。
    这个函数会解析参数，并构建调用实际模型脚本 (main.py) 的具体命令。
    """
    try:
        # 1. 解析从上层传来的JSON参数
        metadata = json.loads(params_json)
        params = metadata.get('advancedParams', {})
        scale = params.get('scale', 4)
        base_channels = params.get('baseChannels', 64)
        bilinear = params.get('bilinear', False)
        model_filename = metadata.get('model', 'unet_best') + '.pth' # 从模型名加上.pth后缀
        model_path = os.path.join(config.MODEL_DIR, model_filename)

        if not os.path.exists(model_path):
            print(f"错误: 模型权重文件未找到于 {model_path}", file=sys.stderr)
            return None

        # 2. 构建调用 `main.py` 的具体命令
        # 这部分逻辑是从旧的 utils.py 中迁移过来的
        cmd = [
            config.PYTHON_PATH, config.SCRIPT_PATH,
            "infer",
            "--checkpoint", model_path,
            "--lr", input_path,
            "--output_dir", output_dir,
            "--lr_scale", str(scale),
            "--base_channels", str(base_channels),
        ]
        if bilinear:
            cmd.append("--bilinear")

        # 3. 执行模型脚本
        print(f"正在执行模型脚本: {' '.join(cmd)}", file=sys.stderr)
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"模型脚本的标准输出: {result.stdout}", file=sys.stderr)

        # 4. 确定输出文件名并验证文件是否存在
        # 这个文件名格式取决于你的 main.py 的输出行为
        input_filename_base = os.path.splitext(os.path.basename(input_path))[0]
        expected_output_filename = f"{input_filename_base}_SR.png"
        expected_output_path = os.path.join(output_dir, expected_output_filename)

        if not os.path.exists(expected_output_path):
            print(f"错误: 预期的输出文件未在路径 {expected_output_path} 中找到", file=sys.stderr)
            return None

        return expected_output_filename

    except subprocess.CalledProcessError as e:
        print(f"模型脚本执行失败。返回码: {e.returncode}", file=sys.stderr)
        print(f"模型脚本的标准错误: {e.stderr}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"在 run_unet_model 中发生意外错误: {str(e)}", file=sys.stderr)
        return None

if __name__ == '__main__':
    # 使用 argparse 来接收来自 utils.py 的参数
    parser = argparse.ArgumentParser(description="UNET 模型的专用启动器。")
    parser.add_argument('--input', required=True, help="输入图片的完整路径。")
    parser.add_argument('--output_dir', required=True, help="保存输出图片的目录。")
    parser.add_argument('--params', required=True, help="包含所有参数的JSON字符串。")
    args = parser.parse_args()

    # 执行推理
    output_filename = run_unet_model(args.input, args.output_dir, args.params)

    if output_filename:
        # ✨ 关键：将最终生成的文件名以特定格式打印到标准输出
        # 上层的 utils.py 会捕获并解析这个输出来识别处理后的文件
        print(f"OUTPUT_FILENAME:{output_filename}")
    else:
        # 如果发生错误，以非零状态码退出，以便上层捕获异常
        sys.exit(1)