"""Functions for handling results"""

from db import db
import users

MAX_ERROR_RATE = 0.05
MIN_TYPING_RATE = 120  # letters per minute.

def get_text_length(exercise_id):
    """Return lenght of the exercise text"""
    sql = "SELECT text_to_write FROM exercises WHERE id=:exercise_id"
    text_length = len(
        db.session.execute(sql, {"exercise_id": exercise_id}).fetchone()[0]
    )
    return text_length

def add_result(exercise_id, used_time, adjusted_time, errors):
    """Method for storing new result to the database"""
    user_id = users.user_id()
    if user_id == 0:
        return False
    text_length=get_text_length(exercise_id)
    typing_speed = text_length * 60 / used_time
    error_rate = errors / text_length
    approved = False
    if typing_speed >= MIN_TYPING_RATE and error_rate <= MAX_ERROR_RATE:
        approved = True
    sql = "INSERT INTO results (user_id, exercise_id, used_time, adjusted_time, errors, approved, sent_at) \
        VALUES (:user_id, :exercise_id, :used_time, :adjusted_time, :errors, :approved, NOW()) RETURNING id"
    db.session.execute(
        sql,
        {
            "user_id": user_id,
            "exercise_id": exercise_id,
            "used_time": used_time,
            "adjusted_time": adjusted_time,
            "errors": errors,
            "approved": approved,
        },
    )
    db.session.commit()
    return True


def seconds_to_time(seconds):
    """Method for converting numeric seconds to hh:mm:ss formatted string"""
    seconds = int(seconds)
    minutes = 0
    hours = 0
    if seconds >= 60:
        minutes = seconds // 60
        seconds -= minutes * 60
        if minutes >= 60:
            hours = minutes // 60
            minutes -= hours * 60
    if seconds < 10 or seconds == 0:
        seconds = "0" + str(seconds)
    if minutes < 10 or minutes == 0:
        minutes = "0" + str(minutes)
    if hours < 10 or hours == 0:
        hours = "0" + str(hours)
    result = str(hours) + ":" + str(minutes) + ":" + str(seconds)
    return result


def get_personal_top10(exercise, text_length):
    """Method for fetching personal top10 results for the given exercise"""
    user = users.user_id()
    sql = "SELECT users.username, results.adjusted_time, results.used_time, results.sent_at, results.errors \
        FROM results LEFT JOIN users ON users.id=results.user_id \
        WHERE user_id=:user_id AND exercise_id=:exercise_id ORDER BY adjusted_time LIMIT 5"
    result = db.session.execute(sql, {"user_id": user, "exercise_id": exercise})
    data = result.fetchall()
    new_data = []
    for i, item in enumerate(data):
        new_data.append({})
        new_data[i]["adjusted_time"] = seconds_to_time(item["adjusted_time"])
        new_data[i]["sent_at"] = item["sent_at"]
        new_data[i]["username"] = item["username"]
        new_data[i]["errors"] = item["errors"]
        new_data[i]["used_time"] = item["used_time"]
        new_data[i]["typing_speed"] = int(
            round(text_length * 60 / item["used_time"], 0)
        )
        new_data[i]["error_rate"] = (
            str(round(item["errors"] / text_length * 100, 1)) + " %"
        )
    return new_data


def get_top10_by_exercise(exercise, text_length):
    """Method for fetching global top10 results for the given exercise"""
    sql = "SELECT users.username, results.adjusted_time, results.used_time, results.sent_at, results.errors \
        FROM results LEFT JOIN users ON users.id=results.user_id \
        WHERE exercise_id=:exercise_id ORDER BY adjusted_time LIMIT 5"
    result = db.session.execute(sql, {"exercise_id": exercise})
    data = result.fetchall()
    new_data = []
    for i, item in enumerate(data):
        new_data.append({})
        new_data[i]["adjusted_time"] = seconds_to_time(item["adjusted_time"])
        new_data[i]["sent_at"] = item["sent_at"]
        new_data[i]["username"] = item["username"]
        new_data[i]["errors"] = item["errors"]
        new_data[i]["used_time"] = item["used_time"]
        new_data[i]["typing_speed"] = int(
            round(text_length * 60 / item["used_time"], 0)
        )
        new_data[i]["error_rate"] = (
            str(round(item["errors"] / text_length * 100, 1)) + " %"
        )
    return new_data


def get_latest_results_by_exercise(exercise, text_length):
    """Method for fetching latest 100 results for the current user for the given exercise"""
    user = users.user_id()
    sql = "SELECT users.username, results.adjusted_time, results.sent_at, results.errors, results.used_time \
        FROM results LEFT JOIN users ON users.id=results.user_id \
        WHERE user_id=:user_id AND exercise_id=:exercise_id ORDER BY sent_at DESC LIMIT 100"
    result = db.session.execute(sql, {"user_id": user, "exercise_id": exercise})
    data = result.fetchall()
    new_data = []
    for i, item in enumerate(data):
        new_data.append({})
        new_data[i]["adjusted_time"] = seconds_to_time(item["adjusted_time"])
        new_data[i]["sent_at"] = item["sent_at"]
        new_data[i]["username"] = item["username"]
        new_data[i]["errors"] = item["errors"]
        new_data[i]["used_time"] = item["used_time"]
        new_data[i]["typing_speed"] = int(
            round(text_length * 60 / item["used_time"], 0)
        )
        new_data[i]["error_rate"] = (
            str(round(item["errors"] / text_length * 100, 1)) + " %"
        )
    return new_data


def is_approved(exercise):
    """Method for checking whether the current user has passed the given exercise"""
    user = users.user_id()
    sql = "SELECT results.adjusted_time, results.used_time, results.sent_at, results.errors, exercises.text_to_write \
        FROM results LEFT JOIN exercises ON exercises.id=results.exercise_id \
        WHERE user_id=:user_id AND exercise_id=:exercise_id ORDER BY adjusted_time LIMIT 1"
    result = db.session.execute(sql, {"user_id": user, "exercise_id": exercise})
    data = result.fetchone()
    if data is None:
        return False
    text_length = len(data["text_to_write"])
    time = int(data["used_time"])
    errors = int(data["errors"])
    typing_rate = text_length * 60 / time
    error_rate = errors / text_length
    if typing_rate > MIN_TYPING_RATE and error_rate < MAX_ERROR_RATE:
        return True
    return False
