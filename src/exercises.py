from db import db
import users

def get_list():
    sql = "SELECT id, name, description, level FROM exercises ORDER BY level"
    result = db.session.execute(sql)
    return result.fetchall()

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

def get_exercise(id):
    sql = "SELECT description, text_to_write, name FROM exercises WHERE id=:id"
    result = db.session.execute(sql, {"id": id}).fetchone()
    return result

def get_tried():
    user_id = users.user_id()

    #TEE TÄMÄ ENSIN
    # sql = "SELECT DISTINCT exercise_id FROM results WHERE user_id=:user_id"
    # result = db.session.execute(sql, {"user_id": user_id}).fetchall()
    # print("exercises", result)

    #HAE sitten näiden levelit. ja laske leveleiden määrä
    # sql = "SELECT DISTINCT level FROM exercises" #toimii
    # sql = "SELECT COUNT (DISTINCT level) FROM exercises" #toimii
    # result = db.session.execute(sql).fetchone()


    # AO TOIMII!
    # SELECT DISTINCT results.exercise_id, exercises.level FROM results LEFT JOIN  exercises ON results.exercise_id=exercises.id WHERE results.user_id=2;
    # print("levels",result)

    print("-------------------")
    sql="SELECT COUNT(DISTINCT results.exercise_id), exercises.level FROM results LEFT JOIN  exercises ON results.exercise_id=exercises.id WHERE results.user_id=:user_id GROUP BY exercises.level;"
    result = db.session.execute(sql, {"user_id": user_id}).fetchall()
    tried={}
    total_tried=0
    for item in result:
        tried[item[1]]=item[0]
        total_tried+=item[0]
    print("tried", tried)

    return (tried, total_tried)


    # print(len(result))
    # return len(result)

def get_passed():
    return None