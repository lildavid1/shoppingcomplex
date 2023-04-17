from flask import Flask, request, render_template, flash, redirect, url_for, jsonify, session
from cs50 import SQL
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mail import Mail, Message
import os 

app = Flask(__name__)

# configure flask mail
app.config["MAIL_DEFAULT_SENDER"] = "ShoppingComplex7@gmail.com"
app.config["MAIL_PASSWORD"] = "gclo rvxn jzpc qhwq"
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "ShoppingComplex7@gmail.com"
mail = Mail(app)

# setting secret key
app.secret_key = os.environ.get("secret_key")

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

db = SQL("sqlite:///project.db")

# setting up session
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
Session(app)

# ensure templates auto reload
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")
def index():
    if "register_id" not in session:
        return redirect("/login")

    products = db.execute("SELECT * FROM products")
    return render_template("homepage.html", products=products)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":

        # select data from onsubmit
        email = request.form.get("email")
        username = request.form.get("username").lower().strip()
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        if not username:
            flash("username is required", category="error")
            return redirect("/login")

        if not password:
            flash("password is required", category="error")
            return redirect("/login")
        
        if password != confirmation:
            flash("Password do not match", category="error")

        # generate password hash
        hash = generate_password_hash(password)
        print(hash)
        
        try:
            # mailing the registrants
            # message = Message("David From Shoppingcomplex.com", recipients=[email])
            # message.body = render_template("email.html")
            # message.html = render_template("email.html", username=username)
            # mail.send(message)

            # insert into database
            db.execute("INSERT INTO registrants (email, username, hash) VALUES(?,?,?)", email, username, hash)

            email = request.form.get("email")
            username = request.form.get("username").lower().strip()
            password = request.form.get("password")
            confirmation = request.form.get("confirmation")

            message = Message("David From Shoppingcomplex.com", recipients=[email])
            message.body = render_template("email.html")
            row = db.execute("SELECT * FROM 'registrants' WHERE email = (?)", email)
            message.html = render_template("email.html", username=username, row=row)
            mail.send(message)

            flash("Account created successfully", category="error")
            return redirect("/login")

        except:

            flash("Credential has already been taken", category="error")
            return redirect("/register")

    flash("Account created successfully", category="error")
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        # collect login information
        username = request.form.get("username").lower().strip()
        password = request.form.get("password")

        rows = db.execute("SELECT * FROM registrants WHERE username = (?)", username)
        
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("Invalid credentials", category="error")
            return redirect("/login")
        
        session["register_id"] = rows[0]["id"]
        print(rows[0]["id"])
        
        return redirect("/")

    return redirect("/login")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/forget", methods=["GET", "POST"])
def update():
    if request.method == "GET":
        return render_template("forget.html")

    if request.method == "POST":
        email = request.form.get("email")

        message = Message("David From Shoppingcomplex.com", recipients=[email])
        message.body = render_template("email.html")    
        message.html = render_template("email.html")
        mail.send(message)


    return render_template("forget.html")
    
@app.route("/product", methods=["GET", "POST"])
def product():
    if "register_id" not in session:
        return redirect("/login")

    if "cart" not in session:
        session["cart"] = []
    
    if request.method == "POST":
        id = request.form.get("id")
        print(id)

        if id:
            session["cart"].append(id)

        return redirect("/product")

    items = db.execute("SELECT * FROM products WHERE id IN (?)", session["cart"])
    return render_template("cart.html", items=items)

@app.route("/remove", methods=["GET", "POST"])
def remove():
    if "register_id" not in session:
        return redirect("/login")
        
    if request.method == "POST":
        id  = request.form.get("id")
        print(id)

        if id:
            session["cart"].remove(id)

            return redirect("/product")

    items = db.execute("SELECT * FROM products WHERE id IN (?)", session["cart"])
    return render_template("cart.html", items=items)
