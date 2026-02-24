# 🎬 AI拍 - 短视频文案脚本创作工具

一个简单易用的桌面应用，用 AI 生成短视频文案脚本！

## ✨ 功能特性

- 🤖 AI 生成短视频文案脚本
- 💾 历史记录保存
- ⭐ 收藏功能
- 🎨 三种风格方案
- ⏱️ 15秒/30秒/60秒时长选择
- 👤 昵称设置
- 💻 纯桌面应用，数据保存在本地

## 🚀 快速开始

### 方式一：直接运行（开发模式）

1. **克隆项目**
```bash
git clone https://github.com/你的用户名/ai_copywriter.git
cd ai_copywriter
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置 API Key**
```bash
# 复制示例配置
cp .env.example .env

# 编辑 .env，填入你的 DeepSeek API Key
# 获取地址：https://platform.deepseek.com/
```

4. **运行应用**
```bash
python app.py
```

### 方式二：打包成安装程序

详见 [使用说明.md](使用说明.md)

## 📝 使用说明

详细使用说明请查看 [使用说明.md](使用说明.md)

## 🛠️ 技术栈

- **后端**: FastAPI + SQLite
- **前端**: HTML + CSS + JavaScript
- **桌面框架**: PyWebView
- **打包工具**: PyInstaller + Inno Setup
- **AI API**: DeepSeek

## 📄 许可证

MIT License

## 🙏 致谢

- [DeepSeek](https://platform.deepseek.com/) - 提供 AI 能力

---

**注意**: 使用前请先配置 DeepSeek API Key！
