import db

def add_item(title, description, target_sum, user_id):
    sql = """INSERT INTO items (title, description, target_sum, user_id)
             VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, description, target_sum, user_id])