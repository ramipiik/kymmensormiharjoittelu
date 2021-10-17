from flask import render_template, request, redirect
from app import app
import messages, users, exercises

@app.route("/")
def index():
    messages_list = messages.get_list()
    exercises_list = exercises.get_list()
    return render_template("index.html", count=len(messages_list), messages=messages_list, exercises=exercises_list)

@app.route("/new")
def new():
    return render_template("new_exercise.html")


@app.route("/exercises/<int:id>")
def exercise(id):
    return render_template("/exercises/exercise"+str(id)+".html")


@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    if messages.send(content):
        return redirect("/")
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut")

@app.route("/new_exercise", methods=["POST"])
def create_exercise():
    name = request.form["name"]
    description = request.form["description"]
    level = request.form["level"]

    if exercises.create(name, level, description):
        return redirect("/")
    else:
        return render_template("error.html", message="Harjoituksen luonti ei onnistunut")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.signup(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")
