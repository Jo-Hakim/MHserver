from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
app = Flask(__name__)
CORS(app, resources={r"/get-password": {"origins": "https://mohammed-hakim.netlify.app"}})
print("installed")
DB_NAME = "articles.db"
MY_PASSWORD = os.getenv("MY_PASSWORD", "default_password")

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()


@app.route("/articles", methods=["GET"])
def get_articles():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content FROM articles")
    rows = cursor.fetchall()
    conn.close()
    articles = [{"id": r[0], "title": r[1], "content": r[2]} for r in rows]
    return jsonify(articles)


@app.route("/articles/<int:article_id>", methods=["GET"])
def get_article(article_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content FROM articles WHERE id=?", (article_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify({"id": row[0], "title": row[1], "content": row[2]})
    return jsonify({"error": "Article not found"}), 404


@app.route("/articles", methods=["POST"])
def add_article():
    data = request.json
    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        return jsonify({"error": "Title and content are required"}), 400

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO articles (title, content) VALUES (?, ?)", (title, content))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({"id": new_id, "title": title, "content": content}), 201


@app.route("/get-password", methods=["POST"])
def checkpassword():
    password=request.get_json()
    user_password=password.get("password")
    if user_password==MY_PASSWORD:
        return jsonify({"validation":True})
    else:
        return jsonify({"validation":False})


if __name__ == "__main__":
    app.run(debug=True)