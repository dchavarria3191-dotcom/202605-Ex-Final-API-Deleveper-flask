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
    return render_template(template_name_or_list="home.html") 


@app.route("/post/list")  
def get_all_posts():
    Connection = get_db_connection()
    cur = Connection.cursor()
    posts = cur.execute("SELECT * FROM posts")
    return render_template(template_name_or_list="post/list.html", post_list=posts)  # Vista


@app.route("/post/<int:post_id>")  
def get_single_posts(post_id):
    Connection = get_db_connection()
    cur = Connection.cursor()
    post = cur.execute("SELECT * FROM posts where id = ?", (post_id,)).fetchone()
    if post is None:
        abort(404)
    return render_template(template_name_or_list="post/single.html", post_single=post)  # Vista

@app.route("/post/create", methods=("GET","POST"))
def create_post():
    if request.method == "GET":
        return render_template("post/create.html")
    if request.method == "POST":
        title=request.form["title_title"]
        content=request.form["content_content"]
        connection = get_db_connection()
        cur = connection.cursor()
        cur.execute("INSERT INTO posts (title, content) values (?, ?)", (title, content))
        connection.commit()
        return redirect(url_for('get_all_posts'))


@app.route("/post/update/<int:post_id>", methods=("GET","POST"))
def update_post(post_id):
    Connection = get_db_connection()
    cur = Connection.cursor()
    post = cur.execute("SELECT * FROM posts where id = ?", (post_id,)).fetchone()
    if post is None:
        abort(404)

    if request.method == "GET":
        return render_template("post/update.html", single_post=post)
    if request.method == "POST":
        title=request.form["title_title"]
        content=request.form["content_content"]
        connection = get_db_connection()
        cur = connection.cursor()
        cur.execute("UPDATE posts SET title = ?, content = ? WHERE id = ?", (title, content, post_id))
        connection.commit()
        return redirect(url_for('get_all_posts'))

