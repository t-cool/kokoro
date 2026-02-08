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

@app.post("/chat")
async def chat(request: ChatRequest):
    if not llm:
        raise HTTPException(status_code=500, detail="Model is not loaded.")
    
    # 傾聴スタイルと短文指定のシステムプロンプト
    system_instr = (
        "あなたは大学の保健室の先生です。ロジャーズ派の傾聴を心がけ、学生の言葉を否定せず共感的に伝えてください。"
        "応答は1〜3文程度で非常に短くしてください。アドバイスは医療的知見に基づきつつも、まずは学生の感情に寄り添うことを最優先してください。"
        "「〜なんですね」「それはお辛かったですね」といった受容的な表現を使い、日本語で答えてください。"
    )
    
    prompt = f"<start_of_turn>user\n{system_instr}\n\n相談内容: {request.message}<end_of_turn>\n<start_of_turn>model\n"
    
    try:
        response = llm(
            prompt, 
            max_tokens=256, # 短文なので制限を絞る
            stop=["<end_of_turn>", "user", "先生:", "学生:"], 
            echo=False, 
            temperature=0.6 # 少し落ち着いた回答にする
        )
        text = response['choices'][0]['text'].strip()
        # 先生： などのプレフィックスがついた場合に削除
        text = text.replace("先生:", "").replace("カウンセラー:", "").strip()
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
