"""Functions for handling exercises"""

from db import db
import users


def add_comment(exercise_id, content):
    """Stores a new comment to the database"""
    user_id = users.user_id()
    if user_id == 0:
        return False

    sql = "INSERT INTO comments (user_id, exercise_id, content, created) \
        VALUES (:user_id, :exercise_id, :content, NOW())"
    db.session.execute(
        sql,
        {"user_id": user_id, "exercise_id": exercise_id, "content": content},
    )
    db.session.commit()
    return True


def get_comments(exercise_id):
    """Fetches comments for a given exercise from the database"""
    sql = "SELECT users.username, comments.content, comments.created FROM comments \
        LEFT JOIN users ON comments.user_id=users.id WHERE exercise_id=:exercise_id \
        ORDER BY created DESC LIMIT 10"
    result = db.session.execute(sql, {"exercise_id": exercise_id})
    data = result.fetchall()
    new_data = []
    for i, item in enumerate(data):
        new_data.append({})
        new_data[i]["created"] = item["created"]
        new_data[i]["username"] = item["username"]
        new_data[i]["content"] = item["content"]
    return new_data


def get_count():
    """Counts the number of comments for a given exercise"""
    user_id = users.user_id()
    sql = "SELECT COUNT(id) FROM comments WHERE user_id=:user_id;"
    result = db.session.execute(sql, {"user_id": user_id}).fetchone()
    return result[0]
