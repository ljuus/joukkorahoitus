import db

def get_all_categories():
    sql = "SELECT title, id FROM categories ORDER BY id"
    result = db.query(sql)

    categories = {}
    for title, id in result:
        categories[title] = id
    return categories

def get_category(item_id):
    sql = """SELECT categories.title from categories, items
             WHERE items.category_id = categories.id AND
                   items.id = ?"""
    result =  db.query(sql, [item_id])
    return result[0]["title"] if result else None

def add_item(title, description, target_sum, user_id, category_id):
    sql = """INSERT INTO items (title, description, target_sum, user_id, category_id)
             VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [title, description, target_sum, user_id, category_id])

def get_items():
    sql = "SELECT id, title FROM items ORDER BY id DESC"
    return db.query(sql)

def get_item(item_id):
    sql = """SELECT items.id,
                    items.title,
                    items.description,
                    items.target_sum,
                    users.username,
                    users.id user_id
             FROM items, users
             WHERE items.user_id = users.id AND
                   items.id = ?"""
    result = db.query(sql, [item_id])
    return result[0] if result else None

def update_item(item_id, title, description):
    sql = """UPDATE items SET title = ?,
                              description = ?
                          WHERE id = ?"""
    return db.execute(sql, [title, description, item_id])

def remove_item(item_id):
    sql = "DELETE FROM donations WHERE donations.item_id = ?"
    db.execute(sql, [item_id])
    sql = "DELETE FROM items WHERE items.id = ?"
    db.execute(sql, [item_id])

def find_items(query):
    sql = """SELECT id, title
             FROM items
             WHERE title LIKE ? OR description LIKE ?
             ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])

def add_donation(user_id, item_id, amount):
    sql = "INSERT INTO donations (user_id, item_id, amount) VALUES (?, ?, ?)"
    db.execute(sql, [user_id, item_id, amount])

def get_donations(item_id):
    sql = """SELECT donations.amount, users.id, users.username
             FROM donations, users
             WHERE donations.item_id = ? AND donations.user_id = users.id
             ORDER BY donations.id DESC"""
    return db.query(sql, [item_id])

def get_donations_sum(item_id):
    sql = "SELECT SUM(amount) FROM donations, items WHERE items.id = donations.item_id AND items.id = ?"
    result = db.query(sql, [item_id])[0][0]
    
    if result:
        return round(result / 100, 2)
    else:
        return None