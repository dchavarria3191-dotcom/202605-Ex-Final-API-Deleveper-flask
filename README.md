# 202605-Ex-Final-API-Deleveper-flask

1.Clonar el repositorio

---bash 
git clone https://github.com/dchavarria3191-dotcom/202605-Ex-Final-API-Deleveper-flask.git
cd 202605-Ex-Final-API-Deleveper-flask/
---

2.Instalar UV

---bash 
uv sync
source .venv/Scripts/activate
uv run flask --app main.py run --debug
---

3.Inicializar BD

--bash
python init.py
sqlite3 basedatos.db
--bash
