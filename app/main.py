import random
from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from cs50 import SQL


app = Flask(__name__)

db = SQL("sqlite:///user.db")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    number1 = random.randint(1,2)
    return render_template("index.html", number = number1)

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

@app.route("/usr_list")
def usr_list():
    rows = db.execute("SELECT rowid,* FROM usr")
    # for row in rows:
    #     if not row["name"]:
    #         row["name"] = ""

    return render_template("usr_list.html", rows = rows)

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