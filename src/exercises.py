from db import db
import users

def get_list():
    sql = "SELECT id, name, description, level FROM exercises ORDER BY level"
    result = db.session.execute(sql)
    return result.fetchall()

def create(name, level, description):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO exercises (name, level, description) VALUES (:name, :level, :description)"
    db.session.execute(sql, {"name":name, "level":level, "description":description})
    db.session.commit()
    return True