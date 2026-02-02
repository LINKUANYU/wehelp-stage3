from fastapi import *
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app=FastAPI()

app.mount("/static", StaticFiles(directory="static"))

@app.get("/", include_in_schema=False)
def index(request: Request):
    return FileResponse("./static/index.html", media_type="text/html")


@app.post("/api/upload")
async def create_post(
    content: str = Form(...),
    image: UploadFile = File(...)
):
    
    filename = image.filename
    img = await image.read()

    print(f"收到文字{content}")
    print(f"收到圖片{filename}，大小{len(img)}bytes")

    return