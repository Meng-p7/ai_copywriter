from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests
import sqlite3
import uuid
from datetime import datetime
import re
import os
import sys
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
    # 可能的 .env 文件位置
    possible_paths = []
    
    # 1. 可执行文件同一目录
    possible_paths.append(os.path.join(BASE_DIR, '.env'))
    
    # 2. 如果是打包后的，尝试 _MEIPASS 目录
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        possible_paths.append(os.path.join(sys._MEIPASS, '.env'))
    
    # 3. 开发环境的当前目录
    possible_paths.append('.env')
    
    # 尝试加载
    for path in possible_paths:
        if os.path.exists(path):
            load_dotenv(path)
            return True
    
    return False

load_env_from_multiple_locations()

# ====================== 配置项（从环境变量读取）======================
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
HOST = os.getenv('HOST', '127.0.0.1')
PORT = int(os.getenv('PORT', 8000))
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# ====================== 获取数据目录 ======================
def get_data_dir():
    data_dir = os.path.join(BASE_DIR, 'data')
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

# ====================== 数据库文件路径 ======================
DB_PATH = os.path.join(get_data_dir(), 'ai_copywriter.db')

# ====================== 验证必要配置 ======================
if not DEEPSEEK_API_KEY:
    raise ValueError("请在 .env 文件中配置 DEEPSEEK_API_KEY")

# 初始化FastAPI应用
app = FastAPI(title="AI文案脚本创作API", version="1.0")

@app.post("/api/test_simple")
def test_simple(req: dict):
    return {
        "code": 200,
        "msg": "测试成功",
        "data": {
            "script_id": "test_123",
            "schemes": ["测试方案1", "测试方案2", "测试方案3"]
        }
    }

# ====================== 获取静态文件目录 ======================
def get_static_dir():
    # 如果是打包后的，优先用 _MEIPASS（临时资源目录）
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    # 否则用基础目录
    return BASE_DIR

STATIC_DIR = get_static_dir()

# 挂载静态文件（前端）
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# 根路径重定向到静态文件
@app.get("/")
def read_root():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/static/index.html")

# 配置CORS（允许跨域请求）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====================== 初始化SQLite数据库 ======================
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建脚本表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scripts (
            id VARCHAR(64) PRIMARY KEY,
            user_id VARCHAR(64) NOT NULL,
            scene VARCHAR(100) NOT NULL,
            style VARCHAR(100) NOT NULL,
            duration VARCHAR(20) NOT NULL,
            key_info TEXT,
            content TEXT NOT NULL,
            schemes TEXT,
            create_time DATETIME NOT NULL,
            update_time DATETIME NOT NULL
        )
    ''')
    
    # 创建收藏表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS favorites (
            id VARCHAR(64) PRIMARY KEY,
            user_id VARCHAR(64) NOT NULL,
            scene VARCHAR(100) NOT NULL,
            style VARCHAR(100) NOT NULL,
            duration VARCHAR(20) NOT NULL,
            key_info TEXT,
            content TEXT NOT NULL,
            scheme_index INTEGER DEFAULT 0,
            scheme_name VARCHAR(50),
            create_time DATETIME NOT NULL
        )
    ''')
    
    # 创建用户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(64) PRIMARY KEY,
            phone VARCHAR(20) UNIQUE,
            nickname VARCHAR(50),
            avatar VARCHAR(255),
            create_time DATETIME NOT NULL,
            update_time DATETIME NOT NULL
        )
    ''')
    
    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_scripts_user ON scripts(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_favorites_user ON favorites(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_phone ON users(phone)')
    
    conn.commit()
    conn.close()

# 初始化数据库
init_db()

# ====================== SQLite连接函数 ======================
def get_db_conn():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"数据库连接失败：{str(e)}")

# ====================== 语料库缓存（优化性能）======================
corpus_cache = {}

def get_cached_corpus(scene):
    if scene in corpus_cache:
        return corpus_cache[scene]
    return None

def set_cached_corpus(scene, content):
    corpus_cache[scene] = content

# DeepSeek API调用函数
def call_deepseek_api(prompt):
    if not DEEPSEEK_API_KEY:
        raise HTTPException(status_code=500, detail="未配置DeepSeek API Key")
    
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 1.3,
        "max_tokens": 2500,
        "stream": False
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        content = result["choices"][0]["message"]["content"].strip()
        return content
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=500, detail="AI响应超时，请稍后重试")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"AI请求失败：{str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI生成失败：{str(e)}")

# 数据模型（新增style和duration字段，带默认值）
class CreateScriptRequest(BaseModel):
    user_id: str
    scene: str
    key_info: str
    brand_corpus_id: str = None
    style: str = "口语化"  # 新增：风格，默认口语化
    duration: str = "30秒"  # 新增：时长，默认30秒

# 数据模型：保存脚本请求
class SaveScriptRequest(BaseModel):
    user_id: str
    scene: str
    key_info: str
    style: str
    duration: str
    content: str

# 新增：根据场景自动生成语料库的函数（带缓存优化）
def generate_corpus_by_scene(scene):
    # 先检查缓存
    cached = get_cached_corpus(scene)
    if cached:
        return cached
    
    prompt = f"""
    请为{scene}创作场景生成一份专业的语料库，包含以下内容：
    1. 该场景常用的爆款词汇和表达（10-15个）
    2. 该场景常用的句式和开场白（5-8个）
    3. 该场景的情绪调动技巧和互动话术（5-8个）
    4. 该场景的行业术语和常用说法

    请直接输出内容，不要任何多余的格式。
    """
    try:
        content = call_deepseek_api(prompt)
        # 缓存结果
        set_cached_corpus(scene, content)
        return content
    except:
        return ""

# ------------------- 核心接口：生成文案/脚本 -------------------
@app.post("/api/script/create", response_model=dict)
def create_script(req: CreateScriptRequest):
    # 跳过语料库生成，直接使用简化提示
    corpus_content = "口语化表达，情绪饱满"
    
    # 2. 按时长匹配镜头数量
    duration_map = {
        "15秒": 3,
        "30秒": 6,
        "60秒": 12
    }
    shot_count = duration_map.get(req.duration, 5)
    
    # 3. 风格提示词细化
    style_prompt = {
        "口语化": "语言极度口语化，像和朋友聊天，多用网络热词、语气词（比如：哇、绝了、家人们），节奏快",
        "专业化": "语言专业、严谨，突出产品卖点和数据，适合品牌官方账号，避免口语化表达",
        "搞笑风": "台词幽默搞笑，镜头有反差感、夸张动作，多用梗和段子，让用户笑出声",
        "煽情风": "语言温暖、有感染力，能触动情绪，镜头慢节奏，背景音乐舒缓，适合情感类内容"
    }.get(req.style, "语言口语化，有感染力，适合短视频拍摄")
    
    # 4. 构造AI提示词（生成1种高质量方案）
    prompt = f"""
    你是专业的{req.scene}短视频脚本创作师，请生成1种高质量的{req.duration}短视频文案方案。
    严格遵守以下所有规则，一条都不能违反：

    1. 必须包含核心信息：{req.key_info}
    2. 参考该场景的专业语料库：{corpus_content}
    3. 时长要求：严格控制在{req.duration}，镜头数量为{shot_count}个，每个镜头台词长度匹配时长,字数尽量多
    4. 严禁使用广告违禁词：最、第一、顶级、绝对、全网第一、永久等。
    5. 输出格式：

    标题: 这里写视频标题，一定要足够吸睛
    {"".join([f"镜头{i}: 镜头内容描述\n台词{i}: 台词内容（必须是博主说的话，不能空）\n\n" for i in range(1, shot_count+1)])}
    配乐建议: 统一的背景音乐风格描述（整个视频使用同一首音乐）

    要求：
    - 使用{style_prompt}风格
    - 镜头、台词的编号必须一一对应
    - 每一行只写一项，不要把多个内容写在同一行
    - 不要任何多余格式、表格、横线、星号、加粗符号
    - 台词必须是口语化的句子，不能省略
    - 配乐建议只在方案的最后统一输出一次
    - 充分利用参考语料库中的爆款词汇和表达，让文案更符合该场景的特点
    - 确保文案质量高，有吸引力，能够有效传达核心信息
    """
    
    # 5. 调用AI生成内容
    script_content = call_deepseek_api(prompt)
    
    # 6. 直接使用生成的内容作为单个方案
    schemes = [script_content]
    
    # 7. 保存到数据库（保存所有方案）
    script_id = f"script_{uuid.uuid4().hex[:8]}"
    create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    import json
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO scripts (id, user_id, scene, key_info, style, duration, content, schemes, create_time, update_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (script_id, req.user_id, req.scene, req.key_info, req.style, req.duration, schemes[0] if schemes else "", json.dumps(schemes, ensure_ascii=False), create_time, create_time)
    )
    conn.commit()
    cursor.close()
    conn.close()
    
    # 8. 返回结果
    return {
        "code": 200,
        "msg": "生成成功",
        "data": {
            "script_id": script_id,
            "style": req.style,
            "duration": req.duration,
            "schemes": schemes,
            "create_time": create_time
        }
    }

# ------------------- 新增接口：获取历史记录 -------------------
@app.get("/api/scripts/history")
def get_history(user_id: str, limit: int = 20):
    import json
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, scene, key_info, style, duration, content, schemes, create_time FROM scripts WHERE user_id = ? ORDER BY create_time DESC LIMIT ?",
        (user_id, limit)
    )
    rows = cursor.fetchall()
    
    records = []
    for row in rows:
        record = dict(row)
        try:
            schemes_str = record.get('schemes')
            if schemes_str:
                record['schemes'] = json.loads(schemes_str)
            else:
                record['schemes'] = [record.get('content', '')]
        except:
            record['schemes'] = [record.get('content', '')]
        records.append(record)
    
    cursor.close()
    conn.close()
    
    return {
        "code": 200,
        "msg": "获取成功",
        "data": records
    }

# ------------------- 新增接口：删除历史记录 -------------------
@app.delete("/api/scripts/{script_id}")
def delete_script(script_id: str, user_id: str):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM scripts WHERE id = ? AND user_id = ?",
        (script_id, user_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"code": 200, "msg": "删除成功"}

# ------------------- 新增接口：生成数字人视频 -------------------
@app.post("/api/video/generate")
def generate_video(request: dict):
    user_id = request.get('user_id')
    model = request.get('model', '2.0')
    digital_human = request.get('digital_human', 'default')
    voice_style = request.get('voice_style', 'female')
    script = request.get('script', '')

    if not user_id or not script:
        return {"code": 400, "msg": "参数不全"}

    try:
        # 这里需要替换为实际的Sedance API调用
        import requests
        import json

        # 示例：调用Sedance API
        sedance_api_url = "https://api.sedance.com/v1/video/generate"
        sedance_api_key = "YOUR_SEDANCE_API_KEY"  # 需要替换为实际的API Key

        payload = {
            "model": f"sedance-{model}",
            "digital_human": digital_human,
            "voice_style": voice_style,
            "script": script
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {sedance_api_key}"
        }

        # 这里暂时返回模拟数据
        return {
            "code": 200,
            "msg": "视频生成成功",
            "data": {
                "video_url": "https://example.com/video.mp4",
                "model": model,
                "digital_human": digital_human
            }
        }
    except Exception as e:
        return {"code": 500, "msg": f"生成失败: {str(e)}"}

# ------------------- 收藏接口 -------------------
# 添加收藏
@app.post("/api/favorites/add", response_model=dict)
def add_favorite(user_id: str, scene: str, style: str, duration: str, key_info: str, content: str, scheme_index: int = 0, scheme_name: str = None):
    fav_id = f"fav_{uuid.uuid4().hex[:8]}"
    create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO favorites (id, user_id, scene, style, duration, key_info, content, scheme_index, scheme_name, create_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (fav_id, user_id, scene, style, duration, key_info, content, scheme_index, scheme_name, create_time)
    )
    conn.commit()
    cursor.close()
    conn.close()
    
    return {
        "code": 200,
        "msg": "收藏成功",
        "data": {"favorite_id": fav_id}
    }

# 获取收藏列表
@app.get("/api/favorites/list", response_model=dict)
def get_favorites(user_id: str, limit: int = 50):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, scene, style, duration, key_info, content, scheme_index, scheme_name, create_time FROM favorites WHERE user_id = ? ORDER BY create_time DESC LIMIT ?",
        (user_id, limit)
    )
    rows = cursor.fetchall()
    
    favorites = []
    for row in rows:
        favorites.append(dict(row))
    
    cursor.close()
    conn.close()
    
    return {
        "code": 200,
        "msg": "获取成功",
        "data": favorites
    }

# 删除收藏
@app.delete("/api/favorites/{favorite_id}", response_model=dict)
def delete_favorite(favorite_id: str, user_id: str):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM favorites WHERE id = ? AND user_id = ?",
        (favorite_id, user_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    
    return {
        "code": 200,
        "msg": "删除成功"
    }



# 启动服务
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=HOST, port=PORT, reload=DEBUG)