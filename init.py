import sqlite3

Connection = sqlite3.connect("basedatos.db")

with open("schema.sql", "w") as f:
    f.write("""
drop table if exists posts;

create table posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    create_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);
""")

with open("schema.sql", "r") as f:
    Connection.executescript(f.read())


def insert_data(title, content):
    Connection = sqlite3.connect("basedatos.db")
    cur = Connection.cursor()
    cur.execute("INSERT INTO posts (title, content) values (?, ?)", (title, content))
    Connection.commit()
    Connection.close()


insert_data("primer post", "contenido del primer post")
insert_data("segundo post", "contenido del segundo post")
insert_data("tercero post", "contenido del tercero post")
