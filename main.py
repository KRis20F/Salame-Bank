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

@app.route("/Home", methods=["GET", "POST"])
def new_connection():
    if request.method == "POST":
        client = {}

        form_data = request.form
        client["username"] = form_data["username"]
        client["password"] = form_data["password"]

        client = functions.connect_account(client)

        if isinstance(client, dict):
            session["client_info"] = client
            return render_template("Home.html", client_info = client)
        else:
            return render_template("Login.html", error_message = client)
        
    elif request.method == "GET":
        if "client_info" in session:
            client_info = session["client_info"]
            client_info = functions.connect_account(client_info)
            
            return render_template("Home.html", client_info = client_info)
        else:
            return render_template("Login.html")

@app.route("/Confirmed", methods=["POST"])
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
        return render_template("Signin.html", error_message = "Error de conexión, intentalo más tarde")

@app.route("/deposit")
def deposit_section():
    return render_template("deposit.html")

@app.route("/Completed", methods=["POST"])
def manage_money():
    form_data = request.form

    action = form_data["action"]
    password = form_data["password"]
    money = form_data["money"]
    
    if action == "deposit":
        is_completed = functions.deposit(session["client_info"], password, money)
        
    elif action == "withdraw":
        is_completed = functions.withdraw(session["client_info"], password, money)
    
    elif action == "transfer":
        receiver = form_data["receiver"]
        is_completed = functions.transfer(session["client_info"], receiver, password, money)

    if is_completed:
        return render_template("Completed.html")
    else:
        return render_template("deposit.html", error_message = "Datos incorrectos, intentalo de nuevo")

app.run(host='localhost', port=5069, debug=True)