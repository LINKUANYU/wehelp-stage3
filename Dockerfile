FROM python:3.12

WORKDIR /app

# 直接安裝套件到系統路徑，不需建立虛擬環境
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製專案當前目錄下的所有內容到容器的工作目錄
COPY . .

# 告訴容器要監聽的連接埠 (FastAPI 預設為 8000)
EXPOSE 8000

# 保持在前景執行，交給 docker run -d 來處理背景化
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]