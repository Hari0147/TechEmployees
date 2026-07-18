import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATABASE = "employee.db"


# --------------------------
# Database Initialization
# --------------------------
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        department TEXT NOT NULL,
        salary INTEGER NOT NULL
    )
    """)

    conn.commit()
    conn.close()


init_db()


# --------------------------
# Get All Employees
# --------------------------
@app.route("/employees", methods=["GET"])
def get_employees():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employees")

    rows = cursor.fetchall()

    conn.close()

    employees = []

    for row in rows:

        employees.append({
            "id": row[0],
            "name": row[1],
            "department": row[2],
            "salary": row[3]
        })

    return jsonify(employees)


# --------------------------
# Add Employee
# --------------------------
@app.route("/employees", methods=["POST"])
def add_employee():

    data = request.get_json()

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO employees(name,department,salary)
        VALUES(?,?,?)
        """,
        (
            data["name"],
            data["department"],
            data["salary"]
        )
    )

    conn.commit()

    employee_id = cursor.lastrowid

    conn.close()

    return jsonify({
        "message": "Employee Added Successfully",
        "id": employee_id
    }), 201


# --------------------------
# Update Employee
# --------------------------
@app.route("/employees/<int:id>", methods=["PUT"])
def update_employee(id):

    data = request.get_json()

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE employees
        SET
            name=?,
            department=?,
            salary=?
        WHERE id=?
    """,
    (
        data["name"],
        data["department"],
        data["salary"],
        id
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Employee Updated Successfully"
    })


# --------------------------
# Delete Employee
# --------------------------
@app.route("/employees/<int:id>", methods=["DELETE"])
def delete_employee(id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM employees WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Employee Deleted Successfully"
    })


# --------------------------
# Get Single Employee
# --------------------------
@app.route("/employees/<int:id>", methods=["GET"])
def get_employee(id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM employees WHERE id=?",
        (id,)
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return jsonify({"message": "Employee Not Found"}), 404

    return jsonify({
        "id": row[0],
        "name": row[1],
        "department": row[2],
        "salary": row[3]
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )
