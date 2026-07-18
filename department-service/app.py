import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATABASE = "department.db"


# --------------------------
# Database Initialization
# --------------------------
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            department_name TEXT NOT NULL UNIQUE
        )
    """)

    # Insert default departments only once
    cursor.execute("SELECT COUNT(*) FROM departments")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany(
            "INSERT INTO departments (department_name) VALUES (?)",
            [
                ("Development",),
                ("DevOps",),
                ("Testing",),
                ("HR",),
                ("Finance",),
                ("Support",)
            ]
        )

    conn.commit()
    conn.close()


init_db()


# --------------------------
# Get All Departments
# --------------------------
@app.route("/departments", methods=["GET"])
def get_departments():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM departments")

    rows = cursor.fetchall()

    conn.close()

    departments = []

    for row in rows:
        departments.append({
            "id": row[0],
            "department_name": row[1]
        })

    return jsonify(departments)


# --------------------------
# Get One Department
# --------------------------
@app.route("/departments/<int:id>", methods=["GET"])
def get_department(id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM departments WHERE id=?",
        (id,)
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return jsonify({"message": "Department Not Found"}), 404

    return jsonify({
        "id": row[0],
        "department_name": row[1]
    })


# --------------------------
# Add Department
# --------------------------
@app.route("/departments", methods=["POST"])
def add_department():

    data = request.get_json()

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO departments (department_name) VALUES (?)",
        (data["department_name"],)
    )

    conn.commit()

    department_id = cursor.lastrowid

    conn.close()

    return jsonify({
        "message": "Department Added Successfully",
        "id": department_id
    }), 201


# --------------------------
# Update Department
# --------------------------
@app.route("/departments/<int:id>", methods=["PUT"])
def update_department(id):

    data = request.get_json()

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE departments
        SET department_name=?
        WHERE id=?
        """,
        (
            data["department_name"],
            id
        )
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Department Updated Successfully"
    })


# --------------------------
# Delete Department
# --------------------------
@app.route("/departments/<int:id>", methods=["DELETE"])
def delete_department(id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM departments WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Department Deleted Successfully"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5002,
        debug=True
    )
