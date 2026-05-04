from flask import Flask, render_template

app = Flask(__name__)


@app.route("/index") # Controlador
def home():
    base_de_datos = ["Adrian","Karen","Thanitos"] # Modelos o BD
    return render_template(template_name_or_list="index.html", datos=base_de_datos) # Vista