# fffeng99999/rgzn-gcsj-qianduan/rgzn-gcsj-qianduan-1380fd747a3f68c1ae28cea72052197a6290bc74/server/utils/model_runner.py
import os
import subprocess
import time

def run_inference(app_config, input_path, metadata):
    """
    使用从前端接收的参数调用外部模型推理脚本。
    修改后，此函数从 app_config 读取所有必需的路径。
    """
    try:
        # 从 app.config 获取路径
        output_dir = app_config['PROCESSED_FOLDER']
        model_dir = app_config['MODEL_DIR']
        python_path = app_config['PYTHON_PATH']
        script_path = app_config['SCRIPT_PATH']

        # 从 metadata 中读取参数，设置默认值
        params = metadata.get('advancedParams', {})
        scale = params.get('scale', 4)
        base_channels = params.get('baseChannels', 128)
        bilinear = params.get('bilinear', False)
        model_filename = metadata.get('model', 'unet_best.pth')

        # 构建模型文件的完整路径
        model_path = os.path.join(model_dir, model_filename)
        if not os.path.exists(model_path):
            print(f"错误：模型文件不存在：{model_path}")
            return None, 0

        # 构建命令行
        cmd = [
            python_path, script_path, "infer",
            "--checkpoint", model_path,
            "--lr", input_path,
            "--output_dir", output_dir,
            "--lr_scale", str(scale),
            "--base_channels", str(base_channels),
        ]
        if bilinear:
            cmd.append("--bilinear")

        print(f"执行命令: {' '.join(cmd)}")

        # 执行并计时
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8')
        duration = time.time() - start_time

        print(f"推理成功（耗时: {duration:.2f}s）")
        print(f"脚本输出: {result.stdout}")

        # 根据输入文件名确定输出文件名，这与旧代码逻辑保持一致
        input_filename_base = os.path.splitext(os.path.basename(input_path))[0]
        expected_output_filename = f"{input_filename_base}_SR.png"
        processed_path = os.path.join(output_dir, expected_output_filename)

        if not os.path.exists(processed_path):
            print(f"错误：推理脚本执行成功，但找不到预期的输出文件：{processed_path}")
            # 尝试从 stdout 中寻找线索
            if result.stdout and "Saved LR and SR for" in result.stdout:
                print("请检查 main.py 脚本中的输出文件名逻辑是否与此处预期一致。")
            return None, 0

        return expected_output_filename, duration

    except subprocess.CalledProcessError as e:
        print(f"脚本运行出错! 返回码: {e.returncode}")
        print(f"错误信息 (stderr): {e.stderr}")
        print(f"输出信息 (stdout): {e.stdout}")
        return None, 0
    except Exception as e:
        print(f"运行模型时发生未知错误: {str(e)}")
        return None, 0