from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from llama_cpp import Llama
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

app = FastAPI()

# CORSを許可
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# モデルのパス
MODEL_PATH = "medgemma-4b-it-Q4_K_M.gguf"

print(f"Loading model from {MODEL_PATH}...")
try:
    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=2048,
        n_gpu_layers=-1,
        verbose=False
    )
    print("Model loaded successfully.")
except Exception as e:
    print(f"Failed to load model: {e}")
    llm = None

class ChatRequest(BaseModel):
    message: str
    history: list = []

@app.post("/chat")
async def chat(request: ChatRequest):
    if not llm:
        raise HTTPException(status_code=500, detail="Model is not loaded.")
    
    # 医学的診断と対話による絞り込みを重視したシステムプロンプト
    system_instr = (
        "あなたは学校の保健室に勤務する経験豊富な医師（校医）です。学生の訴えに対して、一度に大量の情報を提示するのではなく、"
        "問診を通じて段階的に原因を絞り込んでください。以下の手順を厳守してください：\n"
        "1. 学生の訴えから、まず可能性のある医学的背景をいくつか推測する。\n"
        "2. その推測を裏付ける、あるいは否定するために、最も重要な質問を【一つだけ】学生に投げかける。\n"
        "3. 学生からの回答を待ってから、次のステップ（さらなる質問、または診断の提示）に進む。\n"
        "4. 最終的な診断と具体的な改善策（生活習慣、受診勧奨など）を提示するまで、この対話を繰り返す。\n"
        "回答は常に簡潔（2〜3文程度）に保ち、医師として論理的で信頼できる口調（〜です、〜してください）を使用してください。"
        "MEDGEMMAの医学的専門知識を背景に持ちつつも、対話を通じて慎重に原因を特定していくプロセスを重視してください。"
    )
    
    # 履歴の構築（システム指示を最初に含める）
    prompt = f"<start_of_turn>user\n{system_instr}<end_of_turn>\n"
    
    for msg in request.history:
        role = "user" if msg['role'] == 'user' else "model"
        # 最初の挨拶は履歴に含まれている可能性があるので重複を避ける（必要なら）
        prompt += f"<start_of_turn>{role}\n{msg['text']}<end_of_turn>\n"
    
    prompt += f"<start_of_turn>user\n{request.message}<end_of_turn>\n<start_of_turn>model\n"
    
    try:
        response = llm(
            prompt, 
            max_tokens=512, # 医学的説明のために拡張
            stop=["<end_of_turn>", "user", "先生:", "学生:", "<start_of_turn>"], 
            echo=False, 
            temperature=0.4 # より正確で落ち着いた回答にする
        )
        text = response['choices'][0]['text'].strip()
        # 先生： などのプレフィックスがついた場合に削除
        text = text.replace("先生:", "").replace("校医:", "").replace("医師:", "").strip()
        return {"response": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ルートおよび index.html へのアクセスを処理
@app.get("/")
@app.get("/index.html")
async def read_index():
    if os.path.exists("index.html"):
        return FileResponse('index.html')
    raise HTTPException(status_code=404, detail="index.html not found")

# main.js へのアクセスを処理
@app.get("/main.js")
async def read_js():
    if os.path.exists("main.js"):
        return FileResponse('main.js')
    raise HTTPException(status_code=404, detail="main.js not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
