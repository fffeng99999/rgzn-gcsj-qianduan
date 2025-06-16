# logger.py
import json
import config  # 导入我们的配置文件


def log_request_data(filename, metadata):
    """
    将接收到的请求数据记录到控制台和 JSON 文件中。

    Args:
        filename (str): 上传文件的名称。
        metadata (dict): 随请求接收到的 JSON 元数据。
    """
    # 1. 记录到控制台以便开发期间即时反馈
    print("--- 正在记录前端数据 ---")
    print(f"收到的图像文件名: {filename}")
    # 使用 json.dumps 将字典漂亮地打印到控制台
    pretty_metadata = json.dumps(metadata, indent=2, ensure_ascii=False)
    print(f"收到的元数据 JSON: {pretty_metadata}")
    print("-----------------------------")

    # 2. 将元数据保存到专用日志文件
    try:
        # 使用 'w' 模式在每次请求时覆盖文件。
        # 如果要保留历史记录，请使用 'a'（追加）模式。
        # 对于此用例（记录*最后*一次请求的元数据），'w' 是正确的。
        with open(config.LOG_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=4)
        print(f"已成功将元数据保存到 {config.LOG_FILE_PATH}")
    except IOError as e:
        print(f"将元数据保存到日志文件时出错: {e}")
    except Exception as e:
        # 捕获文件 I/O 期间的其他潜在异常
        print(f"写入日志文件时发生意外错误: {e}")