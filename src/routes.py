"""Module for handling URL calls"""

from flask import render_template, request, redirect, session, abort
from app import app
import users
import exercises
import results
import comments


@app.route("/")
def index():
    """Returns the main page"""
    exercises_list = exercises.get_list()
    total = len(exercises_list)
    levels = exercises.get_levels()
    comment_count = comments.get_count()
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
    """Returns the admin page"""
    exercises_list = exercises.get_list()
    stats = exercises.get_stats()
    if users.is_admin():
        return render_template("admin.html", exercises=exercises_list, stats=stats)
    return render_template("error.html", message="Access denied")


@app.route("/edit/<int:exercise_id>")
def edit(exercise_id):
    """Returns the page for editing a single exercise"""
    if users.is_admin():
        exercise = exercises.get_exercise(exercise_id)
        return render_template("edit.html", exercise=exercise)
    return render_template("error.html", message="Access denied")


@app.route("/delete", methods=["POST"])
def delete():
    """Handles delete requests"""
    data = request.get_json()
    csrf_received = data["csrf_token"]
    if csrf_received != session["csrf_token"]:
        print("csrf_tokens don't match")
        abort(403)
    exercise_id = data["id"]
    if users.is_admin():
        exercises.delete(exercise_id)
        return True
    return render_template("error.html", message="Access denied")


@app.route("/exercises/<int:exercise_id>")
def single_exercise(exercise_id):
    """Return the page for a single exercise"""
    exercise_data = exercises.get_exercise(exercise_id)
    description = exercise_data["description"]
    text_to_write = exercise_data["text_to_write"]
    name = exercise_data["name"]
    text_length = len(text_to_write)
    personal_top10 = results.get_personal_top10(str(exercise_id), text_length)
    latest_results = results.get_latest_results_by_exercise(
        str(exercise_id), text_length
    )
    top10 = results.get_top10_by_exercise(str(exercise_id), text_length)
    comments_data = comments.get_comments(str(exercise_id))

    approved = results.is_approved(str(exercise_id))
    return render_template(
        "/exercise.html",
        personal_top10=personal_top10,
        top10=top10,
        latest_results=latest_results,
        id=exercise_id,
        description=description,
        text_to_write=text_to_write,
        name=name,
        approved=approved,
        comments=comments_data,
        nr_of_comments=len(comments_data),
        csfr_token=session["csrf_token"],
    )


@app.route("/new_exercise", methods=["POST"])
def create_exercise():
    """Handles request to create a new exercise"""
    name = request.form["name"]
    if len(name) < 1 or len(name) > 40:
        return render_template(
            "error.html", message="Exercise name must be 1-40 characters long"
        )
    description = request.form["description"]
    level = request.form["level"]
    text_to_write = request.form["text_to_write"]
    csrf_received = request.form["csrf_token"]

    if len(description) < 1 or len(description) > 100:
        return render_template(
            "error.html", message="Description must be 1-100 characters long"
        )
    try:
        level = int(level)
    except:
        return render_template(
            "error.html", message="Level must be a number between 0 and 10"
        )
    if level < 0 or level > 10:
        return render_template(
            "error.html", message="Level must be a number between 0 and 10"
        )
    if len(text_to_write) < 3 or len(text_to_write) > 1000:
        return render_template(
            "error.html", message="Text to write must be 3-1000 characters long"
        )
    if "\n" in text_to_write:
        return render_template(
            "error.html",
            message="Sorry, line breaks are not allowed in the exercise text. \
            That's because the algorithm for checking typos cannot handle them properly. :|",
        )
    if csrf_received != session["csrf_token"]:
        print("csrf_tokens don't match")
        abort(403)
    if exercises.create(name, level, description, text_to_write):
        return redirect("/admin")
    return render_template("error.html", message="Harjoituksen luonti ei onnistunut")


@app.route("/edit_exercise", methods=["POST"])
def edit_exercise():
    """Handles requests for editing an exercise"""
    exercise_id = request.form["id"]
    name = request.form["name"]
    if len(name) < 1 or len(name) > 40:
        return render_template(
            "error.html", message="Exercise name must be 1-40 characters long"
        )
    description = request.form["description"]
    if len(description) < 1 or len(description) > 100:
        return render_template(
            "error.html", message="Description must be 1-100 characters long"
        )
    level = request.form["level"]
    try:
        level = int(level)
    except:
        return render_template(
            "error.html", message="Level must be a number between 0 and 10"
        )
    if level < 0 or level > 10:
        return render_template(
            "error.html", message="Level must be a number between 0 and 10"
        )
    text_to_write = request.form["text_to_write"]
    if len(text_to_write) < 3 or len(text_to_write) > 1000:
        return render_template(
            "error.html", message="Text to write must be 3-1000 characters long"
        )
    if "\n" in text_to_write:
        return render_template(
            "error.html",
            message="Sorry, line breaks are not allowed in the exercise text. \
            That's because the algorithm for checking typos cannot handle them properly. :|",
        )
    csrf_received = request.form["csrf_token"]
    if csrf_received != session["csrf_token"]:
        print("csrf_tokens don't match")
        abort(403)
    if exercises.edit(exercise_id, name, level, description, text_to_write):
        return redirect("/admin")
    return render_template(
        "error.html",
        message="Something went wrong. It was not possible to edit the exercise",
    )


@app.route("/new_result", methods=["POST"])
def add_result():
    """Handles requests for adding a new result"""
    data = request.get_json()
    csrf_received = data["csrf_token"]
    if csrf_received != session["csrf_token"]:
        print("csrf_tokens don't match")
        abort(403)
    exercise_id = data["exercise_id"]
    used_time = data["used_time"]
    adjusted_time = data["adjusted_time"]
    errors = data["errors"]
    try:
        exercise_id = int(exercise_id)
        used_time = int(used_time)
        used_time = int(adjusted_time)
        errors = int(errors)
    except:
        return render_template("error.html", message="Hmm. Something went wrong. :|")
    if results.add_result(exercise_id, used_time, adjusted_time, errors):
        return redirect("/")
    return render_template("error.html", message="Could not store the result")


@app.route("/login", methods=["POST"])
def login():
    """Handles login requests"""
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        return redirect("/")
    return render_template("error.html", message="Incorrect username or password")


@app.route("/comment", methods=["POST"])
def comment():
    """Handles requests for posting new comments"""
    content = request.form["new_comment"]
    if len(content) < 1 or len(content) > 400:
        return render_template(
            "error.html", message="Comment must be 1-400 characters long"
        )
    exercise_id = request.form["exercise_id"]
    csrf_received = request.form["csrf_token"]
    if csrf_received != session["csrf_token"]:
        print("csrf_tokens don't match")
        abort(403)
    if comments.add_comment(exercise_id, content):
        return redirect(request.referrer)
    return render_template("error.html", message="Hmmm. Couldn't add the comment. :|")


@app.route("/logout")
def logout():
    """Logs out the current user"""
    users.logout()
    return redirect("/")


@app.route("/signup", methods=["POST"])
def signup():
    """Handles signup requests"""
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if len(username) < 2 or len(username) > 20:
        return render_template(
            "error.html", message="Username must be 2-20 characters long"
        )
    if len(password1) < 2 or len(password1) > 20:
        return render_template(
            "error.html", message="Password must be 2-20 characters long"
        )
    if password1 != password2:
        return render_template("error.html", message="Passwords are not equal")
    if users.signup(username, password1):
        return redirect("/")
    return render_template("error.html", message="User with that name already exists.")
