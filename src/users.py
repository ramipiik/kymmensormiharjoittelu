from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT id, username, is_admin, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    print("user", user)
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            print("user_id", user.id)
            print("username", user.username)
            print("is_admin", user.is_admin)
            session["user_id"] = user.id
            session["username"] = user.username
            session["admin"] = user.is_admin
            return True
        else:
            return False

def logout():
    del session["user_id"]

def signup(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id",0)

def is_admin():
    if session["admin"]==True:
        return True
    return False
    # print("is_admin")
    # print("type(is_admin)", type(user))

