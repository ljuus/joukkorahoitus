from werkzeug.security import check_password_hash, generate_password_hash
import db

def check_login(username, password):
    sql = "SELECT id, username,  password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    db.execute(sql, [username])

    if len(result) == 1:
        user_id, username, password_hash = result[0]
        if check_password_hash(password_hash, password):
            return (user_id, username)
    
    return None

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = " INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])