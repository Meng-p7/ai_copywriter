# 🎬 AI拍 - 短视频文案脚本创作工具

一个简单易用的桌面应用，用 AI 生成短视频文案脚本！

## ✨ 功能特性

- 🤖 AI 生成短视频文案脚本
- 💾 历史记录保存
- ⭐ 收藏功能
- 🎨 三种风格方案
- ⏱️ 15秒/30秒/60秒时长选择
- 👤 昵称设置
- 🔄 自动检查更新
- 💻 纯桌面应用，数据保存在本地

## 🚀 快速开始

### 方式一：直接运行（开发模式）

1. **克隆项目**
```bash
git clone https://github.com/Meng-p7/ai_copywriter.git
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

## 📦 开发者：发布新版本

当你有新功能要发布时，按以下步骤操作：

### 1. 更新版本号

修改 `index.html` 中的版本号：
```javascript
const APP_VERSION = "1.0.1"; // 更新为新版本号
const GITHUB_REPO = "Meng-p7/ai_copywriter"; // 改成你的用户名
```

### 2. 提交代码

```bash
git add .
git commit -m "发布 v1.0.1"
git push
```

### 3. 在 GitHub 创建 Release

1. 访问你的 GitHub 仓库
2. 点击右侧的 "Releases"
3. 点击 "Draft a new release"
4. **Tag version**: 填 `v1.0.1`（注意前面加 v）
5. **Release title**: 填 `v1.0.1`
6. **Describe this release**: 写更新内容（比如：新增了 XX 功能，修复了 XX 问题）
7. 把打包好的 `AI拍_安装程序.exe` 拖到附件区域
8. 点击 "Publish release"

### 4. 用户收到更新

用户打开应用时，会自动检查 GitHub Releases，如果有新版本就会弹出提示，点击"去下载"就能跳转到你的 Release 页面下载！

---

**注意**: 使用前请先配置 DeepSeek API Key！
