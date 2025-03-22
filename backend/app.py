from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import os
import time

app = Flask(__name__)
CORS(app)

DB_HOST = os.getenv("DB_HOST", "mysql-container")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "flask_board")

# MySQL 연결 함수 (재시도 로직 포함)
def connect_db():
    for _ in range(10):  # 최대 10번 재시도
        try:
            conn = pymysql.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                cursorclass=pymysql.cursors.DictCursor
            )
            return conn
        except Exception as e:
            print(f"⏳ MySQL 연결 대기... {e}")
            time.sleep(3)
    raise Exception("❌ MySQL 연결 실패!")

conn = connect_db()

# 테이블 자동 생성
def create_table():
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255),
                content TEXT
            );
        """)
        conn.commit()

create_table()

@app.route('/posts', methods=['GET'])
def get_posts():
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM posts ORDER BY id DESC")
        posts = cursor.fetchall()
    return jsonify(posts)

@app.route('/posts', methods=['POST'])
def create_post():
    data = request.json
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO posts (title, content) VALUES (%s, %s)", (data['title'], data['content']))
        conn.commit()
    return jsonify({'message': '게시글이 추가되었습니다.'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
