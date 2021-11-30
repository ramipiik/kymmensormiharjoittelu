from db import db
import users


def add_comment(exercise_id, content):
    user_id = users.user_id()
    if user_id == 0:
        return False

    sql = "INSERT INTO comments (user_id, exercise_id, content, created) VALUES (:user_id, :exercise_id, :content, NOW())"
    db.session.execute(
        sql,
        {"user_id": user_id, "exercise_id": exercise_id, "content": content},
    )
    db.session.commit()
    return True


def get_comments(exercise_id):
    sql = "SELECT users.username, comments.content, comments.created FROM comments LEFT JOIN users ON comments.user_id=users.id WHERE exercise_id=:exercise_id ORDER BY created DESC LIMIT 10"
    result = db.session.execute(sql, {"exercise_id": exercise_id})
    data = result.fetchall()
    newData = []
    for i, item in enumerate(data):
        newData.append({})
        newData[i]["created"] = item["created"]
        newData[i]["username"] = item["username"]
        newData[i]["content"] = item["content"]
    return newData


def get_count():
    user_id = users.user_id()
    # TO DO: Do the the calculation directly in the SQL query
    sql = "SELECT COUNT(id) FROM comments WHERE user_id=:user_id;"
    result = db.session.execute(sql, {"user_id": user_id}).fetchone()
    return result[0]
