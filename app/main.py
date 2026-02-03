from fastapi import *
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uuid
from dotenv import load_dotenv
load_dotenv()
from app.s3_utils import upload_s3
from app.database import get_conn, get_cur


app=FastAPI()

app.mount("/static", StaticFiles(directory="app/static"))

@app.get("/", include_in_schema=False)
def index(request: Request):
    return FileResponse("./app/static/index.html", media_type="text/html")


@app.post("/api/upload")
async def create_post(
    content: str = Form(...),
    image: UploadFile = File(...),
    conn = Depends(get_conn)
):
    
    file_extension = image.filename.split('.')[-1] # 抓最後一個副檔名
    file_name = f"{uuid.uuid4()}.{file_extension}" # 組一個不會撞名的檔名
    
    # 直接將 image.file (檔案物件) 傳給 S3 工具函數
    img_url = upload_s3(image.file, file_name)
    if not img_url:
        raise HTTPException(status_code=500, detail='Fail to upload to S3')

    try:
        cur = conn.cursor()
        sql = "INSERT INTO comments(content, image_url) VALUES(%s, %s)"
        cur.execute(sql, (content, img_url))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"資料庫寫入失敗: {e}")
    finally:
        cur.close()

    return {"ok":True}

@app.get("/api/get-post")
def get_post(cur = Depends(get_cur)):
    try:
        cur.execute("SELECT content, image_url FROM comments ORDER BY created_at ASC")
        rows = cur.fetchall()
        if not rows:
            return {"data": None}
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"資料庫查詢失敗: {e}")