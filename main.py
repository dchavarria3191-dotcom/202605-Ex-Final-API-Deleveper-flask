from flask import Flask, redirect, render_template, request, url_for, abort

app = Flask(__name__)


@app.route("/")  # Controlador
def root():
    return render_template(template_name_or_list="base.html")  # Vista


@app.route("/index")  # Controlador
def index():
    base_de_datos = ["Adrian", "Karen", "Thanitos"]  # Modelos o BD
    return render_template(
        template_name_or_list="index.html", datos=base_de_datos
    )  # Vista


@app.route("/home")  # Controlador
def home():
    return render_template(template_name_or_list="home.html")  # Vista
