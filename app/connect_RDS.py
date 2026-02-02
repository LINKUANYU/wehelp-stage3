from dbutils.pooled_db import PooledDB
import pymysql

POOL = PooledDB(
    creator=pymysql,  # 使用 PyMySQL 作為驅動
    maxconnections=5,  # 連線池最大連線數
    mincached=2,       # 初始化時，池中至少存在的空閒連線數
    host='wehelp-training.cl4y8qec8sg0.ap-east-2.rds.amazonaws.com',
    user='admin',
    password='',
    database='first_db',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor,
    blocking=True      # 連線池滿了時，是否要等待（True 為等待）
)

def get_conn():
    return POOL.connection()

def test():
    conn = get_conn()
    cur = conn.cursor()
    try:
        create_sql = """
        CREATE TABLE IF NOT EXISTS comments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            content TEXT NOT NULL,
            image_url VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) CHARACTER SET utf8mb4;
        """
        cur.execute(create_sql)
        print("TABLE 建立成功")

        cur.execute("INSERT INTO comments (username, content) VALUES (%s, %s)", ('kuan', '我的留言'))
        conn.commit()
        print("留言寫入成功")

        cur.execute("SELECT * FROM comments")
        print("目前資料庫內容", cur.fetchone())
    except Exception as e:
        print(f"錯誤{e}")
    finally:
        cur.close()
        conn.close()

test()