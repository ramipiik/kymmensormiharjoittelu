from flask import render_template, request, redirect
import json
from app import app
import messages, users, exercises, results

@app.route("/")
def index():
    messages_list = messages.get_list()
    exercises_list = exercises.get_list()
    total=len(exercises_list)
    levels=exercises.get_levels()
    tried=exercises.get_tried()
    passed=exercises.get_passed()
    total_passed=len(passed)
    passed_by_level=exercises.get_passed_by_level()
    return render_template("index.html", count=len(messages_list), messages=messages_list, exercises=exercises_list, levels=levels, total=total, tried=tried[0], total_tried=tried[1], passed=passed, total_passed=total_passed, passed_by_level=passed_by_level)

@app.route("/new")
def new():
    return render_template("new_exercise.html")


@app.route("/exercises/<int:id>")
def exercise(id):
    exercise_data=exercises.get_exercise(id)
    description=exercise_data[0]
    text_to_write=exercise_data[1]
    name=exercise_data[2]
    text_length=len(text_to_write)
    # print("length:", text_length)

    personal_top10=results.get_personal_top10(str(id), text_length)
    latest_results=results.get_latest_results_by_exercise(str(id), text_length)
    top10=results.get_top10(str(id), text_length)
    
    approved=results.is_approved(str(id))
    return render_template("/exercise.html", personal_top10=personal_top10, top10=top10, latest_results=latest_results, id=id, description=description, text_to_write=text_to_write, name=name, approved=approved)


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
    text_to_write = request.form["text_to_write"]

    if exercises.create(name, level, description, text_to_write):
        return redirect("/")
    else:
        return render_template("error.html", message="Harjoituksen luonti ei onnistunut")

@app.route("/new_result", methods=["POST"])
def add_result():
    data = request.get_json()
    exercise_id = data["exercise_id"]
    used_time=data["used_time"]
    adjusted_time=data["adjusted_time"]
    errors=data["errors"]
    if results.add_result(exercise_id, used_time, adjusted_time, errors):
        return redirect("/")
    else:
        return render_template("error.html", message="Could not store the result")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # print("username", username)
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
