# fffeng99999/rgzn-gcsj-qianduan/rgzn-gcsj-qianduan-1380fd747a3f68c1ae28cea72052197a6290bc74/server/routes/__init__.py
from .api import api_bp
from .image import image_bp
from .test import test_bp

# 使用 __all__ 明确声明可以从这个包导出哪些变量
# 当其他文件使用 from server.routes import * 时，只会导入 api_bp, image_bp, test_bp
__all__ = ['api_bp', 'image_bp', 'test_bp']