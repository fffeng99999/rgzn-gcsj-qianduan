优化目录结构：

```angular2html
server/
├── __init__.py           # 使 'server' 成为一个 Python 包
├── config.py             # 全局配置
├── main.py               # 应用程序入口 (原 app.py)
├── routes/               # API 路由定义
│   ├── __init__.py       # 定义蓝图，并导入各个模块的路由
│   ├── image_routes.py   # 处理图片上传、处理等相关路由 (原 routes.py 中的大部分)
│   ├── model_routes.py   # 处理模型参数、模型列表等相关路由 (原 routes.py 中新增的)
│   └── report_routes.py  # 处理报告相关的路由 (原 routes.py 中新增的)
├── services/             # 业务逻辑层和功能性服务
│   ├── __init__.py
│   ├── image_service.py  # 图像处理核心逻辑 (原 utils.py 中的 process_image_with_params, resize_image)
│   ├── model_manager.py  # 模型管理、加载参数、选择 runner (原 utils.py 中与模型选择相关的部分)
│   ├── report_service.py # 报告生成服务 (原 report_generator.py)
│   └── utils.py          # 通用工具函数 (原 utils.py 中与业务逻辑无关的辅助函数，如 allowed_file)
├── runners/              # 模型执行器 (更名自 model_runners)
│   ├── __init__.py       # 可用于注册 runners
│   ├── unet_runner.py    # (原 model_runners/unet_best.py 更名)
│   ├── z_demo_runner.py  # (原 model_runners/z-demo.py 更名)
│   └── (其他模型runner)
├── data/                 # 静态数据文件 (非代码文件)
│   ├── uploads/          # 上传图片
│   ├── processed/        # 处理后图片
│   ├── md_parameters/    # 模型预设参数
│   │   ├── unet_best.json
│   │   └── z-demo.json
│   └── logs/             # 日志文件目录 (原 log.json 移动到此处)
│       └── request.log   # 记录请求元数据的日志文件 (原 log.json 更名)
└── assets/               # 静态资源，如字体文件
    └── simsun.ttf        # 字体文件
```