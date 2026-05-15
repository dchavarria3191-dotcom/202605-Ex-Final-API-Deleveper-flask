from flask import Flask, redirect, render_template, request, url_for, abort, jsonify
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect("basedatos.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    return render_template("home.html")


# =========================
# LISTAR ESTUDIANTES
# =========================
@app.route("/students")
def get_all_students():

    connection = get_db_connection()
    cur = connection.cursor()

    students = cur.execute(
        "SELECT * FROM students ORDER BY id DESC"
    ).fetchall()

    connection.close()

    # HTMX
    if request.headers.get("HX-Request"):

        return render_template(
            "partials/students_table.html",
            student_list=students
        )

    return render_template(
        "post/list.html",
        student_list=students
    )


# =========================
# PARTIAL HTMX
# =========================
@app.route("/students/table")
def students_table_partial():

    connection = get_db_connection()
    cur = connection.cursor()

    students = cur.execute(
        "SELECT * FROM students ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "partials/students_table.html",
        student_list=students
    )


# =========================
# PROMEDIO
# =========================
@app.route("/students/average")
def students_average():

    connection = get_db_connection()
    cur = connection.cursor()

    result = cur.execute(
        "SELECT AVG(grade) as average_grade FROM students"
    ).fetchone()

    connection.close()

    average = round(result["average_grade"], 2) if result["average_grade"] else 0

    # HTMX
    if request.headers.get("HX-Request"):

        return f"""
        <div class="alert alert-info mt-3">
            <strong>Promedio de notas:</strong> {average}
        </div>
        """

    return jsonify({
        "average_grade": average
    })


# =========================
# DETALLE
# =========================
@app.route("/students/<int:student_id>")
def get_single_student(student_id):

    connection = get_db_connection()
    cur = connection.cursor()

    student = cur.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()

    connection.close()

    if student is None:
        abort(404)

    return render_template(
        "post/single.html",
        student=student
    )


# =========================
# CREAR
# =========================
@app.route("/students/create", methods=["GET", "POST"])
def create_student():

    if request.method == "GET":
        return render_template("post/create.html")

    dni = request.form["dni"]
    name = request.form["name"]
    age = request.form["age"]
    grade = request.form["grade"]
    is_approved = request.form["is_approved"]

    connection = get_db_connection()
    cur = connection.cursor()

    cur.execute(
        """
        INSERT INTO students (
            dni,
            name,
            age,
            grade,
            is_approved
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (dni, name, age, grade, is_approved)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("get_all_students"))


# =========================
# ACTUALIZAR
# =========================
@app.route("/students/update/<int:student_id>", methods=["GET", "POST"])
def update_student(student_id):

    connection = get_db_connection()
    cur = connection.cursor()

    student = cur.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()

    if student is None:
        connection.close()
        abort(404)

    if request.method == "GET":

        connection.close()

        return render_template(
            "post/update.html",
            student=student
        )

    dni = request.form["dni"]
    name = request.form["name"]
    age = request.form["age"]
    grade = request.form["grade"]
    is_approved = request.form["is_approved"]

    cur.execute(
        """
        UPDATE students
        SET
            dni = ?,
            name = ?,
            age = ?,
            grade = ?,
            is_approved = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (
            dni,
            name,
            age,
            grade,
            is_approved,
            student_id
        )
    )

    connection.commit()
    connection.close()

    return redirect(
        url_for("get_single_student", student_id=student_id)
    )


# =========================
# DELETE PAGE
# =========================
@app.route("/students/delete/<int:student_id>", methods=["GET"])
def delete_student_page(student_id):

    connection = get_db_connection()
    cur = connection.cursor()

    student = cur.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()

    connection.close()

    if student is None:
        abort(404)

    return render_template(
        "post/delete.html",
        student=student
    )


# =========================
# DELETE
# =========================
@app.route("/students/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):

    connection = get_db_connection()
    cur = connection.cursor()

    cur.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    connection.commit()
    connection.close()

    return redirect(
        url_for("get_all_students")
    )


# =========================
# BULK INSERT
# =========================
@app.route("/students/bulk", methods=["GET", "POST"])
def bulk_insert_students():

    if request.method == "GET":
        return render_template("post/bulk.html")

    data = request.get_json()

    if not isinstance(data, list):

        return jsonify({
            "error": "Se esperaba una lista"
        }), 400

    connection = get_db_connection()
    cur = connection.cursor()

    for student in data:

        cur.execute(
            """
            INSERT INTO students (
                dni,
                name,
                age,
                grade,
                is_approved
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                student["dni"],
                student["name"],
                student["age"],
                student["grade"],
                student["is_approved"]
            )
        )

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Bulk insert realizado correctamente"
    })


if __name__ == "__main__":
    app.run(debug=True)
