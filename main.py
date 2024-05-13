import functions, db, os
from flask import Flask, render_template, request, session, redirect, url_for

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

@app.route('/logout')
def logout():
    session.pop('client_info', None)  
    return redirect(url_for('index'))

@app.route("/Home", methods=["GET", "POST"]) # Menu principal del usuario para realizar las operaciones
def new_connection():
    if request.method == "POST": # Si estas iniciando sesion:
        client = {}

        data = request.form
        client["username"] = data["username"]
        client["password"] = data["password"]

        client = functions.connect_account(client)

        if isinstance(client, dict): # Si "client" es un diccionario, contiene los datos del usuario
            session["client_info"] = client
            transactions = functions.check_transactions(client)
            
            return render_template("Home.html", client_info = client, transactions_info = transactions)
        else:
            return render_template("Login.html", error_message = client)
        
    elif request.method == "GET":
        if "client_info" in session: # Si ya tienes una sesion iniciada:
            client_info = session["client_info"]

            # Refresca los nuevos datos tras las operaciones realizadas
            transactions = functions.check_transactions(client_info)
            client_info = functions.connect_account(client_info)
            
            return render_template("Home.html", client_info = client_info, transactions_info = transactions)
        else:
            return render_template("Login.html", error_message = "Error de conexion, vuelve a iniciar sesion")

@app.route("/Confirmed", methods=["POST"]) # Envio de informacion del usuario a la base de datos
def new_client():
    client = {}

    data = request.form
    client["name"] = data["name"]
    client["surname"] = data["surname"]
    client["age"] = data["age"]
    client["country"] = data["country"]
    client["email"] = data["email"]
    
    client["username"] = data["username"]
    client["password"] = data["password"]
    
    is_created = functions.register_client(client)

    if is_created:
        return render_template("Confirmed.html")
    else:
        return render_template("Signin.html", error_message = "Error de conexión, intentalo más tarde")

@app.route("/deposit")
def deposit_section():
    return render_template("deposit.html")

@app.route("/withdraw")
def withdraw_section():
    return render_template("withdraw.html")

@app.route("/transfer")
def transfer_section():
    return render_template("transfer.html")

@app.route("/Completed", methods=["POST"]) # Envio de la operacion del usuario a la base de datos
def manage_money():
    data = request.form

    action = data["action"]
    password = data["password"]
    money = data["money"]
    
    if action == "deposit":
        is_completed = functions.deposit(session["client_info"], password, money)

        if not is_completed:
            return render_template("deposit.html", error_message = "Datos incorrectos, intentalo de nuevo")
        
    elif action == "withdraw":
        is_completed = functions.withdraw(session["client_info"], password, money)

        if not is_completed:
            return render_template("withdraw.html", error_message = "Datos incorrectos, intentalo de nuevo")
    
    elif action == "transfer":
        receiver = data["receiver"]
        is_completed = functions.transfer(session["client_info"], receiver, password, money)

        if not is_completed:
            return render_template("transfer.html", error_message = "Datos incorrectos, intentalo de nuevo")

    return render_template("Completed.html")

app.run(host='localhost', port=5069, debug=True)
