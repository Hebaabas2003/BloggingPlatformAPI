from flask import Flask, jsonify, request
import sqlite3
from datetime import datetime
import json

app = Flask(__name__)

DATABASE = "blog.db"


def create_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT NOT NULL,
            tags TEXT NOT NULL,
            createdAt TEXT NOT NULL,
            updatedAt TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


@app.route("/")
def home():
    return jsonify({
        "message": "Blogging Platform API is running"
    })


@app.route("/posts", methods=["POST"])
def create_post():
    data = request.get_json()

    title = data.get("title")
    content = data.get("content")
    category = data.get("category")
    tags = data.get("tags")

    if not title or not content or not category or not tags:
        return jsonify({
            "error": "title, content, category and tags are required"
        }), 400

    if not isinstance(tags, list):
        return jsonify({
            "error": "tags must be a list"
        }), 400

    now = datetime.utcnow().isoformat() + "Z"

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO posts
        (title, content, category, tags, createdAt, updatedAt)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        title,
        content,
        category,
        json.dumps(tags),
        now,
        now
    ))

    post_id = cursor.lastrowid

    connection.commit()
    connection.close()

    new_post = {
        "id": post_id,
        "title": title,
        "content": content,
        "category": category,
        "tags": tags,
        "createdAt": now,
        "updatedAt": now
    }

    return jsonify(new_post), 201


@app.route("/posts", methods=["GET"])
def get_posts():
    term = request.args.get("term")

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    if term:
        search_term = f"%{term}%"

        cursor.execute("""
            SELECT id, title, content, category, tags, createdAt, updatedAt
            FROM posts
            WHERE title LIKE ?
               OR content LIKE ?
               OR category LIKE ?
        """, (
            search_term,
            search_term,
            search_term
        ))

    else:
        cursor.execute("""
            SELECT id, title, content, category, tags, createdAt, updatedAt
            FROM posts
        """)

    rows = cursor.fetchall()
    connection.close()

    posts = []

    for row in rows:
        post = {
            "id": row[0],
            "title": row[1],
            "content": row[2],
            "category": row[3],
            "tags": json.loads(row[4]),
            "createdAt": row[5],
            "updatedAt": row[6]
        }

        posts.append(post)

    return jsonify(posts), 200


@app.route("/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, content, category, tags, createdAt, updatedAt
        FROM posts
        WHERE id = ?
    """, (post_id,))

    row = cursor.fetchone()
    connection.close()

    if not row:
        return jsonify({
            "error": "Blog post not found"
        }), 404

    post = {
        "id": row[0],
        "title": row[1],
        "content": row[2],
        "category": row[3],
        "tags": json.loads(row[4]),
        "createdAt": row[5],
        "updatedAt": row[6]
    }

    return jsonify(post), 200


@app.route("/posts/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    data = request.get_json()

    title = data.get("title")
    content = data.get("content")
    category = data.get("category")
    tags = data.get("tags")

    if not title or not content or not category or not tags:
        return jsonify({
            "error": "title, content, category and tags are required"
        }), 400

    if not isinstance(tags, list):
        return jsonify({
            "error": "tags must be a list"
        }), 400

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT createdAt
        FROM posts
        WHERE id = ?
    """, (post_id,))

    row = cursor.fetchone()

    if not row:
        connection.close()

        return jsonify({
            "error": "Blog post not found"
        }), 404

    created_at = row[0]
    updated_at = datetime.utcnow().isoformat() + "Z"

    cursor.execute("""
        UPDATE posts
        SET title = ?,
            content = ?,
            category = ?,
            tags = ?,
            updatedAt = ?
        WHERE id = ?
    """, (
        title,
        content,
        category,
        json.dumps(tags),
        updated_at,
        post_id
    ))

    connection.commit()
    connection.close()

    updated_post = {
        "id": post_id,
        "title": title,
        "content": content,
        "category": category,
        "tags": tags,
        "createdAt": created_at,
        "updatedAt": updated_at
    }

    return jsonify(updated_post), 200


@app.route("/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id
        FROM posts
        WHERE id = ?
    """, (post_id,))

    row = cursor.fetchone()

    if not row:
        connection.close()

        return jsonify({
            "error": "Blog post not found"
        }), 404

    cursor.execute("""
        DELETE FROM posts
        WHERE id = ?
    """, (post_id,))

    connection.commit()
    connection.close()

    return "", 204


if __name__ == "__main__":
    create_database()
    app.run(debug=True)