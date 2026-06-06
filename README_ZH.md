# Google Avatar Frame Generator / 谷歌风格头像生成器

[English](README.md) | 简体中文

为您的头像轻松带上辨识度极高的 Google 个人资料四色渐变/分段圆环相框。


## 项目特点

本工具支持在本地浏览器直接运行或通过本地 Python 命令行脚本进行生成：

### 🌐 网页端（Web App）
- **即时交互调整**：支持通过滑块微调彩环粗细、留白间距、头像缩放以及水平/垂直偏移。
- **个性化配色**：提供 4 种彩环配色方案（谷歌经典、黑白极简、赛博霓虹、马卡龙粉）。
- **安全与性能**：全本地浏览器 Canvas 渲染，无需上传任何图片至服务器，极速且隐私安全。

### 🐍 Python 脚本
- **匹配命令行参数**：命令行脚本同步支持自定义彩环比例、留白间距、缩放、偏移及颜色主题。
- **智能运行降级**：内置 Tkinter 文件选择器。若在无 GUI 的终端/服务器环境中运行，会自动转为命令行文件路径输入，保证稳定性。

## 项目结构

- `index.html`：网页结构
- `style.css`：基于 Glassmorphism的高级响应式样式表
- `script.js`：核心 Canvas 渲染、i18n 翻译及交互控制逻辑
- `google_avatar_frame.py`：本地 Python 图像生成脚本
- `requirements.txt`：Python 依赖项列表

## 运行与部署

### 网页端运行
只需将此项目克隆或下载到本地，在项目根目录启动静态服务器即可：
```bash
# 使用 Python 快速启动
python -m http.server 8000
```
启动后在浏览器中访问 `http://localhost:8000` 即可开始使用。项目可以直接部署到 GitHub Pages 等静态托管平台。

### Python 脚本运行
1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. 运行脚本：
   - 默认模式：
     ```bash
     python google_avatar_frame.py
     ```
   - 命令行参数自定义生成模式：
     ```bash
     python google_avatar_frame.py input.png -o output.png --zoom 1.2 --offset-x 0.05 --palette neon
     ```
     使用 `python google_avatar_frame.py --help` 查看完整参数选项。

## 致谢与声明

- **原作者致谢**：特别感谢原项目作者 [2010384626](https://github.com/2010384626) 提供的高质量核心框架与算法。
- **AI 声明**：本项目中网页端的重构美化（Glassmorphism UI 设计、多色彩环、滑块交互、中英文切换机制）以及 Python 脚本命令行参数扩展和无 GUI 环境降级保护，由 Gemini 辅助生成并优化。
