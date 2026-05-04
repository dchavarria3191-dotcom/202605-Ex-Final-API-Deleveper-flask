from flask import Flask, render_template

app = Flask(__name__)

base_de_datos = ["Adrian","Karen","Thanitos"] # Modelos o BD


@app.route("/index") # Controlador
def home():
    return render_template(template_name_or_list="index.html") # Vista