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


@app.route("/home")  # Controlador
def home():
    Connection = get_db_connection()
    cur = Connection.cursor()
    posts = cur.execute("SELECT * FROM posts")
    return render_template(template_name_or_list="home.html", post_list=posts)  # Vista

@app.route("/post/create", methods=("GET","POST"))
def create_post():
    if request.method == "GET":
        return render_template("create.html")
    if request.method == "POST":
        title=request.form["title_title"]
        content=request.form["content_content"]
        connection = get_db_connection()
        cur = connection.cursor()
        cur.execute("INSERT INTO posts (title, content) values (?, ?)", (title, content))
        connection.commit()
        return redirect(url_for('home'))


