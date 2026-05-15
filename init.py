import sqlite3

# Crear conexión
connection = sqlite3.connect("basedatos.db")

# Crear schema.sql
with open("schema.sql", "w") as f:
    f.write("""
DROP TABLE IF EXISTS students;

CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dni TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    grade REAL NOT NULL,
    is_approved BOOLEAN NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
""")

# Ejecutar script SQL
with open("schema.sql", "r") as f:
    connection.executescript(f.read())

connection.close()


def insert_student(dni, name, age, grade, is_approved):
    connection = sqlite3.connect("basedatos.db")
    cur = connection.cursor()

    cur.execute("""
        INSERT INTO students (
            dni,
            name,
            age,
            grade,
            is_approved
        )
        VALUES (?, ?, ?, ?, ?)
    """, (dni, name, age, grade, is_approved))

    connection.commit()
    connection.close()


# Insertar estudiantes
insert_student("72145698", "Adrian Chavarria", 24, 18.5, True)
insert_student("74581236", "Maria Lopez", 22, 15.0, True)
insert_student("78451239", "Carlos Ramirez", 21, 10.5, False)
insert_student("79874512", "Fernanda Torres", 23, 17.2, True)

print("Base de datos creada correctamente")