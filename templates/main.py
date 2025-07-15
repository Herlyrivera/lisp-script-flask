from flask import Flask, request, render_template, redirect, url_for
import os, json

app = Flask(__name__)
os.makedirs("scripts", exist_ok=True)
DB = "scripts/list.json"

if not os.path.exists(DB):
    with open(DB, "w") as f:
        json.dump([], f)

def load_scripts():
    with open(DB, "r") as f:
        return json.load(f)

def save_scripts(data):
    with open(DB, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        descripcion = request.form.get("descripcion")
        codigo = request.form.get("codigo")
        if nombre and codigo:
            filename = nombre.lower().replace(" ", "-") + ".lsp"
            with open(os.path.join("scripts", filename), "w") as f:
                f.write(codigo)
            data = load_scripts()
            data.append({"nombre": nombre, "descripcion": descripcion, "archivo": filename})
            save_scripts(data)
            return redirect("/")
    data = load_scripts()
    bloques = []
    for i, s in enumerate(data):
        try:
            with open(os.path.join("scripts", s["archivo"])) as f:
                contenido = f.read()
        except:
            contenido = "(error al leer archivo)"
        bloques.append({"id": i, "nombre": s["nombre"], "descripcion": s.get("descripcion", ""), "codigo": contenido})
    return render_template("index.html", bloques=bloques)

@app.route("/delete/<int:item_id>")
def delete(item_id):
    data = load_scripts()
    item = data.pop(item_id)
    try:
        os.remove(os.path.join("scripts", item["archivo"]))
    except:
        pass
    save_scripts(data)
    return redirect("/")

@app.route("/edit/<int:item_id>", methods=["GET", "POST"])
def edit(item_id):
    data = load_scripts()
    item = data[item_id]
    if request.method == "POST":
        nombre = request.form.get("nombre")
        descripcion = request.form.get("descripcion")
        codigo = request.form.get("codigo")
        if nombre and codigo:
            filename = nombre.lower().replace(" ", "-") + ".lsp"
            with open(os.path.join("scripts", filename), "w") as f:
                f.write(codigo)
            os.remove(os.path.join("scripts", item["archivo"]))
            data[item_id] = {"nombre": nombre, "descripcion": descripcion, "archivo": filename}
            save_scripts(data)
            return redirect("/")
    with open(os.path.join("scripts", item["archivo"])) as f:
        codigo = f.read()
    return render_template("edit.html", item=item, codigo=codigo, item_id=item_id)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
