
@echo off
echo 启动后端 Flask 服务...
start cmd /k python .\server\main.py

echo 启动前端 Vue 项目...
cd frontend
start cmd /k npm run dev

echo 前后端已启动。
