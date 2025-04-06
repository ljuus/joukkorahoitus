import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
import config, users, items 

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        return abort(403)

@app.route("/")
def index():
    all_items = items.get_items()
    return render_template("index.html", items=all_items)

@app.route("/find_item")
def find_item():
    query = request.args.get("query")
    if query:
        results = items.find_items(query)
    else:
        query = ""
        results = []
    return render_template("find_item.html", query=query, results=results)

@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    return render_template("show_item.html", item=item)

@app.route("/new_item")
def new_item():
    return render_template("new_item.html")

@app.route("/create_item", methods=["POST"])
def create_item():
    title = request.form["title"]
    description = request.form["description"]
    target_sum = request.form["target_sum"]
    user_id = session["user_id"]

    items.add_item(title, description, target_sum, user_id)
    
    return redirect("/")

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    item = items.get_item(item_id)
    return render_template("edit_item.html", item=item)

@app.route("/update_item", methods=["POST"])
def update_item():
    item_id = request.form["item_id"]
    title = request.form["title"]
    description = request.form["description"]

    items.update_item(item_id, title, description)
    
    return redirect("/item/" + str(item_id))

@app.route("/remove_item/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    if request.method == "GET":
        item = items.get_item(item_id)
        return render_template("remove_item.html", item=item)
    
    if request.method == "POST":
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return "VIRHE: salasanat eivät ole samat"
        
        try:
            users.create_user(username, password1)
            return "Tunnus luotu"
        except sqlite3.IntegrityError:
            return "VIRHE: tunnus on jo varattu"

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user_info = users.check_login(username, password)

        if user_info:
            session["user_id"] = user_info[0]
            session["username"] = user_info[1]
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    require_login()

    del session["user_id"]
    del session["username"]
    return redirect("/")
