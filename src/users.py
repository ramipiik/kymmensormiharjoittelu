"""Functions for handling users"""

import secrets
from flask import session
import sqlalchemy
from werkzeug.security import check_password_hash, generate_password_hash
from db import db


def login(username, password):
    """Logs in a user if password correct"""
    sql = "SELECT id, username, is_admin, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return False
    if check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["username"] = user.username
        session["admin"] = user.is_admin
        session["csrf_token"] = secrets.token_hex(16)
        return True
    return False


def logout():
    """Logs out the user"""
    del session["user_id"]
    del session["username"]
    del session["admin"]
    del session["csrf_token"]


def signup(username, password):
    """Stores a new user to the database"""
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password, created) VALUES (:username,:password, NOW())"
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return False
    return login(username, password)


def user_id():
    """Return user_id of the current user from the browser session"""
    return session.get("user_id", 0)


def is_admin():
    """Checks whether the user has admin rights"""
    if session["admin"]:
        return True
    return False
