# 图像增强与处理演示平台 (qianduan)

**qianduan** 是一个基于 Vue 3 和 Vite 构建的现代单页应用 (SPA)，旨在演示图像的逐步增强和处理过程。它利用 Naive UI 提供美观的用户界面，并集成了实时状态监控和结果可视化功能。

---

## 目录

- 项目概述
- 主要特性
- 技术栈
- 项目结构
- 快速开始
- 推荐 IDE 设置
- 安装依赖
- 运行开发服务器
- 构建生产版本
- 使用指南
- 贡献
- 许可证

---

## 项目概述

本项目是一个用于图像增强和处理的交互式演示平台。用户可以上传图像，选择不同的增强步骤和参数，实时查看处理进度和损失曲线，并最终对比原图与处理结果，甚至下载增强后的图像。整个应用遵循“顶部导航栏、中间内容区、底部页脚”的经典布局，提供直观的用户体验。

---

## 主要特性

- **图像上传与拖放**：支持直观的图像文件上传，并提供全屏拖放区域提示。
- **多种增强模型**：支持选择不同的模型（如通用模型、动漫模型）进行图像处理。
- **分步图像增强**：提供多阶段（如轮廓增强、纹理增强、语义增强）的图像处理流程，用户可以自由选择。
- **高级参数控制**：允许用户调整增强过程中的高级参数，如缩放、基础通道、双线性上采样等。
- **实时状态显示**：在处理过程中，实时展示进度条和损失曲线图，帮助用户了解处理状态。
- **结果可视化与对比**：处理完成后，展示原始图像与增强图像的对比，并提供处理过程的 GIF 动画和质量指标（PSNR、SSIM、CLIP-SCORE）。
- **结果下载**：用户可以下载处理后的图像。
- **响应式布局**：适应不同屏幕尺寸的设备。
- **主题切换**：支持亮色和暗色主题模式切换，提升用户体验。
- **路由管理**：清晰的页面路由结构（主页、演示页、关于页）。
- **Pinia 状态管理**：用于跨组件和页面共享图像处理任务数据。

---

## 技术栈

**前端框架**：
- Vue 3：渐进式 JavaScript 框架。
- Vue Router：Vue.js 的官方路由管理器。
- Pinia：Vue 的下一代状态管理库。

**UI 组件库**：
- Naive UI：一个基于 Vue 3 的全面的、快速的 UI 组件库。

**构建工具**：
- Vite：下一代前端工具，提供极速的开发体验。

**图表库**：
- ECharts：一个强大、交互式、可定制的图表可视化库。

**HTTP 请求**：
- Axios：一个基于 Promise 的 HTTP 客户端。

**语言**：
- TypeScript：JavaScript 的一个超集，提供了静态类型检查。

---

## 项目结构

```
├── public/                 # 静态资源 (不经 Vite 处理)
├── src/                    # 源代码目录
│   ├── assets/             
│   │   ├── base.css
│   │   ├── componentsBarBackground.css
│   │   ├── main.css
│   │   ├── shadows.css
│   │   └── views/
│   │       └── demo-layout.css
│   ├── components/
│   │   ├── ControlPanel4.vue
│   │   ├── FileDropOverlay.vue
│   │   ├── ImagePreview.vue
│   │   ├── ImagePreviewResult.vue
│   │   ├── InputBar2.vue
│   │   ├── ResultsDisplay.vue
│   │   ├── StatusDisplay.vue
│   │   ├── StatusDisplayPreviewResult.vue
│   │   └── TopNavigationBar.vue
│   ├── composables/
│   │   └── useDragAndDrop.js
│   ├── layout/
│   │   └── Layout.vue
│   ├── router/
│   │   └── index.ts
│   ├── store/
│   │   └── enhancementStore.ts
│   ├── views/
│   │   ├── About.vue
│   │   ├── Demo-test5-refresh4.vue
│   │   └── Home.vue
│   ├── App.vue
│   ├── main.ts
│   └── env.d.ts
├── .gitignore
├── index.html
├── package.json
├── package-lock.json
├── README.md
├── tsconfig.json
└── vite.config.ts
```

---

## 快速开始

### 推荐 IDE 设置

- **推荐编辑器**：VS Code
- **插件**：Volar (必须，Vue 3 单文件组件支持)

---

### 安装依赖

```bash
npm install
```

---

### 运行开发服务器

```bash
npm run dev
```

---

### 构建生产版本

```bash
npm run build
```

---

## 使用指南

### 导航

使用顶部的导航栏切换到：

- Home（主页）
- Demo（演示）
- About（关于）

### 图像上传

1. 进入 Demo 页面。
2. 在输入框中拖放图像文件，或点击上传按钮选择文件。
3. 上传成功后，预览图将显示在左侧区域。

### 选择模型与增强步骤

1. 在输入框上方选择：
    - General Model
    - Anime Model
2. 在右侧控制面板中勾选增强步骤（如：Step 1: Outline Enhancement）。
3. 可根据需要调整高级参数。

### 开始处理

1. 输入提示信息（如果需要）。
2. 点击提交按钮，开始图像处理。

### 查看状态

- 处理中：左侧展示实时处理进度和损失曲线图。

### 查看结果

- 完成后：右侧展示原图与增强图对比。
- 包含处理过程的 GIF、PSNR、SSIM、CLIP-SCORE 等。
- 可点击下载增强图像。

---

## 贡献

欢迎任何形式的贡献！  
如有问题或建议，请提交 Issue 或 Pull Request。

---

## 许可证

本项目采用 **MIT 许可证** 发布。
