from db import db
import users

def add_result(exercise_id, used_time, adjusted_time):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO results (user_id, exercise_id, used_time, adjusted_time, sent_at) VALUES (:user_id, :exercise_id, :used_time, :adjusted_time, NOW()) RETURNING id"
    db.session.execute(sql, {"user_id":user_id, "exercise_id":exercise_id, "used_time":used_time, "adjusted_time": adjusted_time})
    db.session.commit()
    return True
