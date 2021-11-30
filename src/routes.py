from flask import render_template, request, redirect
from app import app
import users, exercises, results, comments


@app.route("/")
def index():
    exercises_list = exercises.get_list()
    total = len(exercises_list)
    levels = exercises.get_levels()
    comment_count = comments.get_count()
    print(comment_count)
    tried = exercises.get_tried_by_user()
    passed = exercises.get_passed_by_user()
    total_passed = len(passed)
    passed_by_level = exercises.get_passed_by_level()
    return render_template(
        "index.html",
        exercises=exercises_list,
        levels=levels,
        total=total,
        tried=tried[0],
        total_tried=tried[1],
        passed=passed,
        total_passed=total_passed,
        passed_by_level=passed_by_level,
        comment_count=comment_count,
    )


@app.route("/admin")
def admin():
    exercises_list = exercises.get_list()
    stats = exercises.get_stats()
    if users.is_admin():
        return render_template("admin.html", exercises=exercises_list, stats=stats)
    else:
        return render_template("error.html", message="Access denied")


@app.route("/edit/<int:id>")
def edit(id):
    if users.is_admin():
        exercise = exercises.get_exercise(id)
        return render_template("edit.html", exercise=exercise)
    else:
        return render_template("error.html", message="Access denied")


@app.route("/delete", methods=["POST"])
def delete():
    data = request.get_json()
    id = data["id"]
    if users.is_admin():
        exercises.delete(id)
        return True
    else:
        return render_template("error.html", message="Access denied")


@app.route("/exercises/<int:id>")
def exercise(id):
    exercise_data = exercises.get_exercise(id)
    description = exercise_data["description"]
    text_to_write = exercise_data["text_to_write"]
    name = exercise_data["name"]

    # To do: len can be done in SQL
    text_length = len(text_to_write)

    personal_top10 = results.get_personal_top10(str(id), text_length)
    latest_results = results.get_latest_results_by_exercise(str(id), text_length)
    top10 = results.get_top10_by_exercise(str(id), text_length)
    comments_data = comments.get_comments(str(id))

    approved = results.is_approved(str(id))
    return render_template(
        "/exercise.html",
        personal_top10=personal_top10,
        top10=top10,
        latest_results=latest_results,
        id=id,
        description=description,
        text_to_write=text_to_write,
        name=name,
        approved=approved,
        comments=comments_data,
        nr_of_comments=len(comments_data),
    )


@app.route("/new_exercise", methods=["POST"])
def create_exercise():
    name = request.form["name"]
    description = request.form["description"]
    level = request.form["level"]
    text_to_write = request.form["text_to_write"]
    if exercises.create(name, level, description, text_to_write):
        return redirect("/admin")
    else:
        return render_template(
            "error.html", message="Harjoituksen luonti ei onnistunut"
        )


@app.route("/edit_exercise", methods=["POST"])
def edit_exercise():
    id = request.form["id"]
    name = request.form["name"]
    description = request.form["description"]
    level = request.form["level"]
    text_to_write = request.form["text_to_write"]
    if exercises.edit(id, name, level, description, text_to_write):
        return redirect("/admin")
    else:
        return render_template(
            "error.html",
            message="Something went wrong. It was not possible to edit the exercise",
        )


@app.route("/new_result", methods=["POST"])
def add_result():
    data = request.get_json()
    exercise_id = data["exercise_id"]
    used_time = data["used_time"]
    adjusted_time = data["adjusted_time"]
    errors = data["errors"]
    if results.add_result(exercise_id, used_time, adjusted_time, errors):
        return redirect("/")
    else:
        return render_template("error.html", message="Could not store the result")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        return redirect("/")
    else:
        return render_template("error.html", message="Incorrect username or password")


@app.route("/comment", methods=["POST"])
def comment():
    content = request.form["new_comment"]
    exercise_id = request.form["exercise_id"]
    print(request.referrer)
    if comments.add_comment(exercise_id, content):
        return redirect(request.referrer)
    else:
        return render_template(
            "error.html", message="Hmmm. Couldn't add the comment. :|"
        )


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return render_template("error.html", message="Passwords are not equal")
    if users.signup(username, password1):
        return redirect("/")
    else:
        return render_template("error.html", message="Registration not successful")
