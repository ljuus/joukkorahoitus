import re
import sqlite3
from flask import Flask
from flask import abort, make_response, flash, redirect, render_template, request, session
import config, users, items
import markupsafe
import secrets

app = Flask(__name__)
app.secret_key = config.secret_key

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.template_filter('num_format')
def num_format(value):
    try:
        return f"{float(value):,.2f}"
    except (ValueError, TypeError):
        return value

def require_login():
    if "user_id" not in session:
        return abort(403)
    
def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/")
def index():
    all_items = items.get_items()
    return render_template("index.html", items=all_items)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    items = users.get_items(user_id)
    return render_template("show_user.html", user=user, items=items)

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
    if not item:
        abort(404)
    donations = items.get_donations(item_id)
    donations_sum = items.get_donations_sum(item_id)
    target_sum = item["target_sum"]
    if donations_sum:
        if target_sum - donations_sum <= 0:
            distance = None
        else:
            distance = target_sum - donations_sum
    else:
        distance = target_sum
    category = items.get_category(item_id)
    images = items.get_images(item_id)
    
    return render_template("show_item.html", item=item, donations=donations,
                           category=category, images=images, donations_sum=donations_sum,
                           distance=distance)
                           
@app.route("/new_item")
def new_item():
    return render_template("new_item.html")

@app.route("/create_item", methods=["POST"])
def create_item():
    require_login()
    check_csrf()

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    target_sum = request.form["target_sum"]
    if not re.search("[1-9][0-9]{0,9}", target_sum):
        abort(403)
    category = request.form["category"]
    if category == "":
        category_id = None
    else:
        all_categories = items.get_all_categories()
        if category not in all_categories:
            abort(403)
        category_id = all_categories[category]
    user_id = session["user_id"]

    items.add_item(title, description, target_sum, user_id, category_id)
    
    return redirect("/")

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_item.html", item=item)

@app.route("/images/<int:item_id>")
def edit_images(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    images = items.get_images(item_id)

    return render_template("images.html", item=item, images=images)

@app.route("/add_image", methods=["POST"])
def add_image():
    require_login()
    check_csrf()

    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    
    file = request.files["image"]
    if not file.filename.endswith(".png"):
        flash("VIRHE: väärä tiedostomuoto")
        return redirect("/images/" + str(item_id))

    image = file.read()
    if len(image) > 100 * 1024:
        flash("VIRHE: liian suuri kuva")
        return redirect("/images/" + str(item_id))

    items.add_image(item_id, image)
    flash("Kuva lisätty")
    return redirect("/images/" + str(item_id))

@app.route("/image/<int:image_id>")
def show_image(image_id):
    image = items.get_image(image_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/png")
    return response

@app.route("/remove_images", methods=["POST"])
def remove_images():
    require_login()
    check_csrf()

    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    
    for image_id in request.form.getlist("image_id"):
        items.remove_image(item_id, image_id)
        
    return redirect("/images/" + str(item_id))

@app.route("/update_item", methods=["POST"])
def update_item():
    require_login()
    check_csrf()

    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    description = request.form["description"]
    if not title or not description:
        abort(403)

    items.update_item(item_id, title, description)
    
    return redirect("/item/" + str(item_id))

@app.route("/remove_item/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    require_login()

    item = items.get_item(item_id)
    if item["user_id"] != session["user_id"]:
        abort(403)
    if request.method == "GET":
        return render_template("remove_item.html", item=item)
    
    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))
        
@app.route("/create_donation", methods=["POST"])
def create_donation():
    require_login()
    check_csrf()

    user_id = session["user_id"]
    item_id = request.form["item_id"]
    value = request.form["donation_amount"]
    amount = float(value)
    if amount > 1000000000:
        abort(403)
    items.add_donation(user_id, item_id, amount)
    flash("Lahjoitus onnistui")
    return redirect("/item/" + str(item_id))


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]
        if not username or len(username) > 30:
            abort(403)
        password1 = request.form["password1"]
        if not password1 or len(password1) > 1000:
            abort(403)
        password2 = request.form["password2"]
        if not password2 or len(password2) > 1000:
            abort(403)
        if password1 != password2:
            flash("VIRHE: salasanat eivät ole samat")
            return redirect("/register")

        try:
            users.create_user(username, password1)
            flash("Tunnus luotu")
        except sqlite3.IntegrityError:
            flash("VIRHE: tunnus on jo varattu")
            return redirect("/login")
    return redirect("/")

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
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("VIRHE: väärä tunnus tai salasana")
            return redirect("/login")

@app.route("/logout")
def logout():
    require_login()

    del session["user_id"]
    del session["username"]
    return redirect("/")
