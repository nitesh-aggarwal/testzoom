import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from sqlite3 import datetime


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///user.db")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    return render_template("usr_list.html")

@app.route("/bbye")
def bye():
    return "good bye !"

@app.route("/hello")
def hello():
    name = request.args.get("name1")
    if not name:
        return render_template("fail.html")
    return render_template("hello.html", name = name)

@app.route("/task")
def task():
    if "todos" not in session:
        session["todos"]=[]
    return render_template("task.html", todos = session["todos"])

@app.route("/add", methods = ["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    else:
        todo = request.form.get("task")
        session["todos"].append(todo)
        return redirect("/task")

@app.route("/usr_list", methods = ["GET", "POST"])
def usr_list():
    if request.method == "GET":
        rows = db.execute("SELECT * FROM usr")
        return render_template("usr_list.html", rows = rows)
    else:
        name = request.form.get("name")
        if not name:
            return render_template("sorry.html", message = "NAME")
        email = request.form.get("email")
        if not email:
            email = "Not Avaliable"
        mobile = request.form.get("mobile")
        if not mobile:
            mobile = "Not Avaliable"
        country = request.form.get("country")
        if not country:
            country = "Not Avaliable"
        db.execute("INSERT INTO usr (name, email, mobile, country) VALUES (:name, :email, :mobile, :country)",name = name, email = email, mobile = mobile, country = country)
        return redirect("/usr_list")

@app.route("/add_usr", methods = ["GET", "POST"])
def add_usr():
    if request.method == "GET":
        return render_template("add_usr.html")
    else:
        name = request.form.get("usr_name")
        if not name:
            name = None
        email = request.form.get("usr_email")
        if not email:
            return render_template("sorry.html", message = "email")
        db.execute("INSERT INTO usr (name, email) VALUES (:name1, :email1)",name1 = name, email1 = email)
        return redirect("/usr_list")

if __name__ == '__main__':
    app.run(debug=True)