# routes/__init__.py
# 暂时可以留空，或者用于统一导入所有路由蓝图

from .api import api_bp
from .image import image_bp
from .test import test_bp

# 可选：统一导出所有蓝图，main.py 中可以简化导入
all_blueprints = [api_bp, image_bp, test_bp]
