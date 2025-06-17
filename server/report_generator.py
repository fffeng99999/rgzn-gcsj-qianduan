# server/report_generator.py

import os
import json
from fpdf import FPDF
from flask import url_for
import config

# --- 核心报告生成函数 ---
def generate_report_data(report_id, original_filename, processed_filename, parameters):
    """
    生成详细的报告数据。
    目前使用占位符数据，未来可接入真实模型获取。

    Args:
        report_id (str): 唯一的报告ID，用于生成文件名。
        original_filename (str): 原始图片的文件名。
        processed_filename (str): 主处理流程结束后的最终图片文件名。
        parameters (dict): 处理时使用的参数。

    Returns:
        dict: 包含所有报告数据的字典。
    """

    # === 模型通信接口预留 (Placeholder for Model Interaction) ===
    # 在这里，您未来会调用模型的特定函数来获取真实数据
    # real_metrics = model.get_metrics(...)
    # real_step_images = model.get_step_images(...)
    # real_gif_path = model.generate_gif(...)
    # ---------------------------------------------------------

    # --- 1. 模拟“单步结果对比”图像 ---
    # 假设模型处理后，会生成带步骤名的文件，我们在这里模拟这个过程
    # 注意：这里我们简单地复制最终结果图来模拟，实际应用中它们是不同的文件
    # step1_path = _copy_and_rename_file(processed_filename, f"{report_id}_step1.png")
    # step2_path = _copy_and_rename_file(processed_filename, f"{report_id}_step2.png")
    # step3_path = _copy_and_rename_file(processed_filename, f"{report_id}_step3.png")
    #
    # comparison_images = [
    #     {"label": "原始图像", "url": _get_image_url(original_filename, "uploads")},
    #     {"label": "Step 1 轮廓增强", "url": _get_image_url(os.path.basename(step1_path), "processed")},
    #     {"label": "Step 2 纹理增强", "url": _get_image_url(os.path.basename(step2_path), "processed")},
    #     {"label": "Step 3 语义增强", "url": _get_image_url(os.path.basename(step3_path), "processed")}
    # ]

    if config.USE_REAL_DATA:
        # --- 分支1: 使用真实数据 ---
        # 在此部分，您需要调用真实的模型来获取数据。
        # 注意：您需要确保未来真实数据与模拟数据的格式保持一致。

        print("--- [INFO] 正在使用真实模型数据生成报告 ---")

        # 1. TODO: 调用模型获取真实的“单步结果对比”图像路径
        #    这应该返回一个字典，例如: {'Step 1 轮廓增强': '/path/to/real_step1.png', ...}
        # real_step_images_paths = model.get_step_images(...)
        real_step_images_paths = {}  # 占位符

        # 2. TODO: 调用模型获取真实的 GIF 动画路径
        # real_gif_path = model.generate_gif(...)
        real_gif_path = None  # 占位符

        # 3. TODO: 调用模型获取真实的质量指标
        # real_metrics_data = model.get_metrics(...)
        real_metrics_data = {}  # 占位符

        # --- 准备数据结构 (与模拟数据分支的结构保持一致) ---
        comparison_images = [
            {"label": "原始图像", "url": _get_image_url(original_filename, "uploads")}
        ]
        pdf_image_paths = {
            "原始图像": os.path.join(config.UPLOAD_FOLDER, original_filename)
        }
        for label, path in real_step_images_paths.items():
            comparison_images.append({"label": label, "url": _get_image_url(os.path.basename(path), "processed")})
            pdf_image_paths[label] = path

        gif_url = _get_image_url(os.path.basename(real_gif_path), "processed") if real_gif_path else ""
        metrics = real_metrics_data

    else:
        # --- 分支2: 使用模拟数据 (保留所有现有逻辑) ---
        print("--- [INFO] 正在使用模拟数据生成报告 ---")

        # 1. 模拟“单步结果对比”图像
        comparison_images = [
            {"label": "原始图像", "url": _get_image_url(original_filename, "uploads")}
        ]
        pdf_image_paths = {
            "原始图像": os.path.join(config.UPLOAD_FOLDER, original_filename)
        }
        steps_to_process = parameters.get('steps', {})

        if steps_to_process.get('step1'):
            step1_path = _copy_and_rename_file(processed_filename, f"{report_id}_step1.png")
            if step1_path:
                comparison_images.append({"label": "Step 1 轮廓增强", "url": _get_image_url(os.path.basename(step1_path), "processed")})
                pdf_image_paths["Step 1 轮廓增强"] = step1_path

        if steps_to_process.get('step2'):
            step2_path = _copy_and_rename_file(processed_filename, f"{report_id}_step2.png")
            if step2_path:
                comparison_images.append({"label": "Step 2 纹理增强", "url": _get_image_url(os.path.basename(step2_path), "processed")})
                pdf_image_paths["Step 2 纹理增强"] = step2_path

        if steps_to_process.get('step3'):
            step3_path = _copy_and_rename_file(processed_filename, f"{report_id}_step3.png")
            if step3_path:
                comparison_images.append({"label": "Step 3 语义增强", "url": _get_image_url(os.path.basename(step3_path), "processed")})
                pdf_image_paths["Step 3 语义增强"] = step3_path

        # 2. 模拟 GIF 动画
        mock_gif_path = _copy_and_rename_file(processed_filename, f"{report_id}_animation.gif")
        gif_url = _get_image_url(os.path.basename(mock_gif_path), "processed")

        # 3. 模拟质量指标
        metrics = {
            "PSNR (峰值信噪比)": "32.8 dB",
            "SSIM (结构相似性指数)": "0.95",
            "CLIP-SCORE (语义相似度得分)": "0.88",
            "LPIPS (学习感知图像块相似度)": "0.12"
        }

    # --- 4. 生成PDF报告并获取URL ---
    pdf_filename = f"{report_id}_report.pdf"
    pdf_path = os.path.join(config.PROCESSED_FOLDER, pdf_filename)
    generate_pdf_report(pdf_path, metrics, parameters, pdf_image_paths)
    pdf_url = _get_image_url(pdf_filename, "processed")


    return {
        "comparisonImages": comparison_images,
        "gifUrl": gif_url,
        "metrics": metrics,
        "pdfUrl": pdf_url
    }

def generate_pdf_report(output_path, metrics, params, images_data):
    """使用 metrics 和 params 数据生成一个简单的PDF报告。"""
    pdf = FPDF()
    pdf.add_page()

    # 设置中文字体
    # 注意: 你需要有一个支持中文的字体文件（例如 simsun.ttf）
    # 请下载字体文件并放置在 server/ 目录下
    try:
        # 构建字体的绝对路径
        font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'assets', 'simsun.ttf')
        print(f"--- [调试] 正在加载字体文件于: {font_path}")

        # 在 add_font 方法中使用完整的字体路径
        pdf.add_font('simsun', '', font_path, uni=True)
        pdf.set_font('simsun', '', 14)
    except Exception as e: # 建议捕获更具体的异常或所有异常以进行调试
        print(f"生成报告时出错: {e}")
        # 设置一个备用字体，以防万一
        print("警告: 未找到或无法加载中文字体，PDF 将使用默认字体，可能无法显示中文。")
        pdf.set_font("Arial", size=12)

    pdf.set_font_size(24)
    pdf.cell(200, 10, txt="图像增强详细报告", ln=True, align='C')
    pdf.ln(10)

    # 写入处理参数
    pdf.set_font_size(18)
    pdf.cell(200, 10, txt="处理参数", ln=True)
    pdf.set_font_size(12)
    # 使用 dumps 将 dict 转换为格式化的 JSON 字符串
    params_str = json.dumps(params, indent=2, ensure_ascii=False)
    pdf.multi_cell(0, 5, txt=params_str)
    pdf.ln(5)

    # 写入质量指标
    pdf.set_font_size(18)
    pdf.cell(200, 10, txt="质量评估指标", ln=True)
    pdf.set_font_size(12)
    for key, value in metrics.items():
        pdf.cell(200, 8, txt=f"- {key}: {value}", ln=True)
    pdf.ln(5)

    # --- 写入图片对比结果 ---
    if images_data:
        pdf.add_page()
        pdf.set_font('simsun', '', 18)
        pdf.cell(200, 10, txt="图像结果对比", ln=True, align='C')
        pdf.ln(5)

        for label, path in images_data.items():
            if os.path.exists(path):
                pdf.set_font('simsun', '', 12)
                pdf.cell(0, 10, txt=label, ln=True)
                # 插入图片，w=180表示图片宽度为180mm，高度会自动按比例缩放
                pdf.image(path, w=180)
                pdf.ln(5) # 图片下方留出一些间距
            else:
                print(f"警告：图片文件未找到，无法添加到PDF中: {path}")

    pdf.output(output_path)

# --- 辅助函数 ---
def _get_image_url(filename, folder):
    """安全地生成可从前端访问的URL。"""
    return url_for('main.get_image', folder=folder, filename=filename, _external=True)

def _copy_and_rename_file(original_filename, new_filename):
    """辅助函数，用于复制文件以模拟多步骤输出。"""
    from shutil import copyfile
    source_path = os.path.join(config.PROCESSED_FOLDER, original_filename)
    destination_path = os.path.join(config.PROCESSED_FOLDER, new_filename)
    if os.path.exists(source_path):
        copyfile(source_path, destination_path)
        return destination_path
    return None