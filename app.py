import os
import sys
import threading
import time
import webview
from dotenv import load_dotenv

# ====================== 获取基础目录 ======================
def get_base_dir():
    if getattr(sys, 'frozen', False):
        # 打包后的应用
        return os.path.dirname(sys.executable)
    else:
        # 开发环境
        return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_dir()

# ====================== 加载环境变量（从多个位置尝试）======================
def load_env_from_multiple_locations():
    possible_paths = []
    possible_paths.append(os.path.join(BASE_DIR, '.env'))
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        possible_paths.append(os.path.join(sys._MEIPASS, '.env'))
    possible_paths.append('.env')
    
    for path in possible_paths:
        if os.path.exists(path):
            load_dotenv(path)
            return True
    return False

load_env_from_multiple_locations()

# 导入FastAPI应用
from main import app as fastapi_app
import uvicorn

# 启动FastAPI服务器的线程
def start_server():
    uvicorn.run(
        fastapi_app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )

if __name__ == "__main__":
    # 启动FastAPI服务器（后台线程）
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # 等待服务器启动
    time.sleep(2)
    
    # 启动WebView窗口
    window = webview.create_window(
        title="AI拍 - 短视频文案脚本创作",
        url="http://127.0.0.1:8000/static/index.html",
        width=1200,
        height=800,
        resizable=True,
        min_size=(900, 600),
        text_select=True
    )
    
    webview.start()
