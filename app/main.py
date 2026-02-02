from fastapi import *
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uuid
from dotenv import load_dotenv
load_dotenv()
from s3_utils import upload_s3
from database import get_conn


app=FastAPI()

app.mount("/static", StaticFiles(directory="static"))

@app.get("/", include_in_schema=False)
def index(request: Request):
    return FileResponse("./static/index.html", media_type="text/html")


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