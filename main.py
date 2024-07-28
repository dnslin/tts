from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import edge_tts
import os
import uuid
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源访问，如果你只想允许特定来源，替换 "*" 为指定的 URL
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有请求头
)

class TTSRequest(BaseModel):
    text: str
    voice: str

async def synthesize_tts(text: str, voice: str):
    output_file = f"{uuid.uuid4()}.mp3"
    communicate = edge_tts.Communicate(text=text, voice=voice)
    await communicate.save(output_file)
    return output_file

def remove_file(path: str):
    if os.path.exists(path):
        os.remove(path)

@app.post("/synthesize", response_class=FileResponse)
async def synthesize_post(request: TTSRequest, background_tasks: BackgroundTasks):
    try:
        output_file = await synthesize_tts(request.text, request.voice)
        background_tasks.add_task(remove_file, output_file)
        return FileResponse(output_file, media_type='audio/mpeg', filename=output_file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/synthesize", response_class=FileResponse)
async def synthesize_get(background_tasks: BackgroundTasks,text: str = Query(...), voice: str = Query(...) ):
    try:
        output_file = await synthesize_tts(text, voice)
        background_tasks.add_task(remove_file, output_file)
        return FileResponse(output_file, media_type='audio/mpeg', filename=output_file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/assets", StaticFiles(directory="static/assets"), name="assets")

# 提供主页
@app.get("/")
async def read_index():
    return FileResponse(os.path.join("static", "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8365)
