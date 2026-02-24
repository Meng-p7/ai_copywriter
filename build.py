import os
import sys
import shutil

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 清理旧的构建文件
if os.path.exists('build'):
    shutil.rmtree('build')
if os.path.exists('dist'):
    shutil.rmtree('dist')

print("🚀 开始打包...")

# PyInstaller 配置
import PyInstaller.__main__

PyInstaller.__main__.run([
    # 入口文件
    'app.py',
    
    # 程序名称
    '--name=AI拍',
    
    # 单目录模式（不是单文件，这样启动更快）
    '--onedir',
    
    # 窗口模式（不显示控制台）
    '--windowed',
    
    # 图标
    '--icon=icon.ico',
    
    # 添加数据文件
    '--add-data=index.html;.',
    '--add-data=.env;.',
    
    # 导入隐藏模块
    '--hidden-import=uvicorn.logging',
    '--hidden-import=uvicorn.loops',
    '--hidden-import=uvicorn.loops.auto',
    '--hidden-import=uvicorn.protocols',
    '--hidden-import=uvicorn.protocols.http',
    '--hidden-import=uvicorn.protocols.http.auto',
    '--hidden-import=uvicorn.lifespan',
    '--hidden-import=uvicorn.lifespan.on',
    
    # 不显示控制台（如果需要调试可以注释掉）
    # '--console',
    
    # 清理临时文件
    '--clean',
    
    # 输出目录
    '--distpath=dist',
    '--workpath=build',
    '--specpath=.',
])

print("\n✅ 第一步打包完成！")
print("📦 现在请下载 Inno Setup 来制作安装程序")
print("\n📍 Inno Setup 下载地址：")
print("   https://jrsoftware.org/isdl.php")
print("\n📝 下载后，运行安装程序，然后使用 setup.iss 脚本")

