from db import db
from flask import session
import secrets
from werkzeug.security import check_password_hash, generate_password_hash


def login(username, password):
    sql = "SELECT id, username, is_admin, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            session["admin"] = user.is_admin
            session["csrf_token"] = secrets.token_hex(16)
            return True
        else:
            return False


def logout():
    del session["user_id"]
    del session["username"]
    del session["admin"]
    del session["csrf_token"]


def signup(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password, created) VALUES (:username,:password, NOW())"
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)


def user_id():
    return session.get("user_id", 0)


def is_admin():
    if session["admin"] == True:
        return True
    return False
