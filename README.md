# 🎬 AI拍 - 短视频文案脚本创作工具

一个简单易用的桌面应用，用 AI 生成短视频文案脚本！

## ⚠️ 重要提醒

**改API！改API！改API！**

打开 `.env` 文件，修改你的配置：
```env
DEEPSEEK_API_KEY=你自己的deepseek API
# 获取地址：https://platform.deepseek.com/
```

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
# 编辑 .env，填入你的 DeepSeek API Key


4. **运行应用**
```bash
python app.py
```

### 方式二：打包成安装程序

#### 第一步：打包程序

运行打包脚本：
```bash
python build.py
```

#### 第二步：下载 Inno Setup

1. 访问官网：https://jrsoftware.org/isdl.php
2. 下载最新版本（推荐下载 `innosetup-6.x.x.exe`）
3. 安装 Inno Setup（一路下一步即可）

#### 第三步：制作安装程序

1. 打开 Inno Setup Compiler
2. 点击 File → Open
3. 选择 `setup.iss` 文件
4. 点击 Build → Compile
5. 等待编译完成

完成后，会在 `output` 目录下生成 `AI拍_安装程序.exe`！

#### 第四步：发给朋友

只需要发这一个文件：
```
output/AI拍_安装程序.exe
```

## 🎮 你朋友的使用流程

1. **双击 `AI拍_安装程序.exe`**
2. **选择安装目录**
3. **安装完成，点击"启动 AI拍"**

## 📁 文件说明

```
ai_copywriter/
├── app.py              # 桌面应用启动文件
├── main.py             # FastAPI后端
├── index.html          # 前端页面
├── .env                # 配置文件（API Key）
├── requirements.txt    # 依赖列表
├── build.py            # 打包脚本
├── setup.iss           # 安装程序脚本
├── dist/               # 打包临时文件夹
├── build/              # 构建临时文件夹
├── output/             # 最终安装程序输出目录
└── data/               # 运行时生成的数据库文件夹
```

## 📝 注意事项

### 打包前
- ✅ 确保 `.env` 文件中有正确的 API Key
- ✅ 确保所有依赖都已安装

### 打包后
- ✅ `.env` 文件需要和 `AI拍.exe` 放在同一目录
- ✅ 首次运行会自动创建 `data/ai_copywriter.db` 数据库文件


## 🔧 故障排查

### 问题1：双击 .exe 没反应
- 检查 `.env` 文件是否在同一目录
- 检查 `.env` 文件中的 API Key 是否正确

### 问题2：AI生成失败
- 检查网络连接
- 检查 API Key 是否有效
- 检查 API Key 余额是否充足

### 问题3：打包失败
- 确保所有依赖都已安装：
```bash
pip install -r requirements.txt
```

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

修改 `index.html` 中的版本号，大概在1400行：
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