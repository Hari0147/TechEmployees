import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

DATABASE = "auth.db"


# --------------------------
# Database Initialization
# --------------------------
def init_db():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL

        )
    """)

    conn.commit()
    conn.close()


init_db()


# --------------------------
# Register User
# --------------------------
@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    username = data["username"]
    password = generate_password_hash(data["password"])

    try:

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users(username,password)
            VALUES(?,?)
            """,
            (
                username,
                password
            )
        )

        conn.commit()
        conn.close()

        return jsonify({
            "message": "User Registered Successfully"
        }), 201

    except sqlite3.IntegrityError:

        return jsonify({
            "message": "Username Already Exists"
        }), 400


# --------------------------
# Login
# --------------------------
@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    username = data["username"]
    password = data["password"]

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT password
        FROM users
        WHERE username=?
        """,
        (username,)
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:

        return jsonify({
            "message": "Invalid Username or Password"
        }), 401

    stored_password = row[0]

    if check_password_hash(stored_password, password):

        return jsonify({
            "message": "Login Successful"
        })

    return jsonify({
        "message": "Invalid Username or Password"
    }), 401


# --------------------------
# Get All Users
# --------------------------
@app.route("/users", methods=["GET"])
def get_users():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, username
        FROM users
        """
    )

    rows = cursor.fetchall()

    conn.close()

    users = []

    for row in rows:

        users.append({

            "id": row[0],
            "username": row[1]

        })

    return jsonify(users)


# --------------------------
# Delete User
# --------------------------
@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM users
        WHERE id=?
        """,
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "User Deleted Successfully"
    })


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5003,
        debug=True
    )
