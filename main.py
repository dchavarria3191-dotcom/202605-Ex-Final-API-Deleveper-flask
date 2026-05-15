from flask import Flask, redirect, render_template, request, url_for, abort
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect("basedatos.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")  # Controlador
def root():
    return render_template(template_name_or_list="base.html")  # Vista


@app.route("/home")
def home():
    return render_template(template_name_or_list="base.html")


# LISTAR TODOS LOS ESTUDIANTES
@app.route("/students")
def get_all_students():
    connection = get_db_connection()
    cur = connection.cursor()
    students = cur.execute("SELECT * FROM students").fetchall()
    connection.close()
    return render_template("post/list.html", student_list=students)


# VER DETALLE DE UN ESTUDIANTE
@app.route("/students/<int:student_id>")
def get_single_student(student_id):
    connection = get_db_connection()
    cur = connection.cursor()
    student = cur.execute(
        "SELECT * FROM students WHERE id = ?", (student_id,)
    ).fetchone()
    connection.close()
    if student is None:
        abort(404)
    return render_template("post/single.html", student=student)


@app.route("/students/create", methods=("GET", "POST"))
def create_student():

    # MOSTRAR FORMULARIO
    if request.method == "GET":
        return render_template("post/create.html")

    # GUARDAR ESTUDIANTE
    if request.method == "POST":
        dni = request.form["dni"]
        name = request.form["name"]
        age = request.form["age"]
        grade = request.form["grade"]

        # Checkbox / Select / Input booleano
        is_approved = request.form["is_approved"]

        connection = get_db_connection()
        cur = connection.cursor()

        cur.execute(
            """
            INSERT INTO students (dni,name,age,grade,is_approved) VALUES (?, ?, ?, ?, ?)
            """,
            (dni, name, age, grade, is_approved),
        )

        connection.commit()
        connection.close()

        return redirect(url_for("get_all_students"))


@app.route("/students/update/<int:student_id>", methods=["GET", "POST"])
def update_student(student_id):

    connection = get_db_connection()
    cur = connection.cursor()

    student = cur.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()

    # Verificar existencia
    if student is None:
        connection.close()
        abort(404)

    # Mostrar formulario
    if request.method == "GET":

        connection.close()

        return render_template(
            "post/update.html",
            student=student
        )

    # Actualizar estudiante
    if request.method == "POST":

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
            url_for("get_all_students")
        )
    
# MOSTRAR PANTALLA DE CONFIRMACIÓN PARA ELIMINAR ESTUDIANTE
@app.route("/students/delete/<int:student_id>", methods=["GET"])
def delete_student_page(student_id):

    connection = get_db_connection()
    cur = connection.cursor()

    # Buscar estudiante
    student = cur.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()

    connection.close()

    # Validar existencia
    if student is None:
        abort(404)

    # Mostrar template de confirmación
    return render_template(
        "post/delete.html",
        student=student
    )


# ELIMINAR ESTUDIANTE
@app.route("/students/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):

    connection = get_db_connection()
    cur = connection.cursor()

    # Verificar si existe
    student = cur.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()

    if student is None:
        connection.close()
        abort(404)

    # Eliminar registro
    cur.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    connection.commit()
    connection.close()

    # Redireccionar
    return redirect(
        url_for("get_all_students")
    )

