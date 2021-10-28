from db import db
import users

def get_list():
    sql = "SELECT id, name, description, level FROM exercises ORDER BY level"
    data = db.session.execute(sql).fetchall()

    passed = get_passed()
    new_data=[]
    for i, item in enumerate(data):
        new_data.append([])
        for part in item:
            new_data[i].append(part)
        
        if item[0] in passed:
            new_data[i].append(True)
        else:
            new_data[i].append(False)

    print("new_data", new_data)
    return new_data

def get_levels():
    sql = "SELECT DISTINCT level FROM exercises ORDER BY level"
    result = db.session.execute(sql)
    levels=[]
    for item in result:
        levels.append(item[0])
    return levels

def create(name, level, description, text_to_write):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO exercises (name, level, description, text_to_write) VALUES (:name, :level, :description, :text_to_write)"
    db.session.execute(sql, {"name":name, "level":level, "description":description, "text_to_write": text_to_write})
    db.session.commit()
    return True

def delete(id):
    if users.is_admin(): 
        sql = "DELETE FROM exercises WHERE id=:id"
        db.session.execute(sql, {"id":id})
        db.session.commit()
        return True

def get_exercise(id):
    sql = "SELECT description, level, text_to_write, name, id FROM exercises WHERE id=:id"
    result = db.session.execute(sql, {"id": id}).fetchone()
    return result

def edit(id, name, level, description, text_to_write):
    print("-----------------")
    print("id", id, "name", name, "level", level, "desriptin", description, "text_to_write", text_to_write)
    print("-----------------")
    level=int(level)
    sql = "UPDATE exercises SET name=:name, level=:level, description=:description, text_to_write=:text_to_write WHERE id=:id"
    db.session.execute(sql, {"id": id, "description": description, "text_to_write": text_to_write, "level": level, "name": name})
    db.session.commit()
    return True

def get_tried():
    user_id = users.user_id()
    sql="SELECT COUNT(DISTINCT results.exercise_id), exercises.level FROM results LEFT JOIN  exercises ON results.exercise_id=exercises.id WHERE results.user_id=:user_id GROUP BY exercises.level;"
    result = db.session.execute(sql, {"user_id": user_id}).fetchall()
    tried={}
    total_tried=0
    for item in result:
        tried[item[1]]=item[0]
        total_tried+=item[0]

    print("tried", tried)
    return (tried, total_tried)

def get_passed():
    user_id = users.user_id()
    sql="SELECT DISTINCT r.exercise_id FROM results r WHERE r.user_id=:user_id AND r.approved=True";
    data = db.session.execute(sql, {"user_id": user_id}).fetchall()
    result=[]
    for item in data:
        result.append(item[0])
    return result

def get_passed_by_level():
    user_id = users.user_id()
    sql="SELECT COUNT(DISTINCT results.exercise_id), exercises.level FROM results LEFT JOIN  exercises ON results.exercise_id=exercises.id WHERE results.user_id=:user_id and results.approved=True GROUP BY exercises.level;"
    result = db.session.execute(sql, {"user_id": user_id}).fetchall()
    passed={}
    for item in result:
        passed[item[1]]=item[0]

    # print("passed2", passed)
    return (passed)