import functions, db, os
from flask import Flask, render_template, request, session;

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/")
def index():
    db.create_database()
    return render_template("index.html")

@app.route("/Login")
def login():
    return render_template("Login.html")

@app.route("/Signin")
def signin():
    return render_template("Signin.html")

@app.route("/Home", methods=("POST",))
def new_connection():
    client = {}

    form_data = request.form
    client["username"] = form_data["username"]
    client["password"] = form_data["password"]

    client = functions.connect_account(client)

    if type(client) is dict:
        session["client_info"] = client
        return render_template("Home.html", client_info = client)
    else:
        return render_template("Login.html", error = client)


@app.route("/Confirmed", methods=("POST",))
def new_client():
    client = {}

    form_data = request.form
    client["name"] = form_data["name"]
    client["surname"] = form_data["surname"]
    client["age"] = form_data["age"]
    client["country"] = form_data["country"]
    client["email"] = form_data["email"]
    
    client["username"] = form_data["username"]
    client["password"] = form_data["password"]
    
    is_created = functions.register_client(client)

    if is_created:
        return render_template("Confirmed.html")
    else:
        return render_template("Signin.html", error = "el servidor esta caido, intentalo más tarde")

@app.route("/deposit")
def deposit_section():
    return render_template("deposit.html")

@app.route("/Completed", methods=("POST",))
def deposit_money():
    form_data = request.form

    password = form_data["password"]
    money = form_data["money"]
    
    is_completed = functions.deposit(session["client_info"], password, money)

    if is_completed:
        return render_template("Completed.html")
    else:
        return render_template("deposit.html")

        
app.run(host='localhost', port=5069, debug=True)