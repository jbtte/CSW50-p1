import os

from flask import Flask, session, request, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def login():
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/confirmation", methods=["POST"])
def confirmation():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    user_id = request.form.get("username")
    email = request.form.get("email")
    passw = request.form.get("password")

    # Make sure user doesn't already exists.
    if db.execute("SELECT * FROM users WHERE id = :id", {"id": user_id}).rowcount != 0:
        return render_template("error.html", message="User already exists.")
    db.execute("INSERT INTO users (id, password, name, surname, email) VALUES (:id, :password, :name, :surname, :email)",
            {"id":user_id, "password":passw, "name":first_name, "surname":last_name, "email":email})
    db.commit()
    return render_template("success.html")

@app.route("/logcheck", methods=["POST"])
def logcheck():

    user_id = request.form.get("username")
    passw = request.form.get("password")

    user_passw = db.execute("SELECT password FROM users WHERE id = :id", {"id": user_id}).fetchone()


    if user_passw[0] != passw:
        return render_template("error.html", message="User/Password combination doesn't match. Please try again.")
    else:
        return render_template("search.html")

@app.route("/lookup", methods=["POST"])
def lookup():

    search_param = request.form.get("search_param")

    search_result = db.execute("SELECT * FROM books WHERE isbn ILIKE :text OR title ILIKE :text OR author ILIKE :text",
    {"text": "%"+search_param+"%"}).fetchall()

    #return render_template("test.html", search_result=search_result)

    return render_template("lookup.html", search_result=search_result)
