import functions, db
from flask import Flask, render_template, request;

app = Flask(__name__)

# Declaración de rutas de la aplicación web
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

@app.route("/Home", methods=('GET', 'POST'))
def new_connection():
    client = {}

    if request.method == ('POST'):
        form_data = request.form
        client["username"] = form_data['username']
        client["password"] = form_data['password']

        client = functions.connect_account(client)

        if client:
            return render_template("Home.html", client_info = client)

        else:
            return render_template("Login.html", login = False, error = client)

@app.route("/Confirmed", methods=('GET', 'POST'))
def new_client():
    client = {}

    if request.method == 'POST':
        form_data = request.form
        client["name"] = form_data["name"]
        client["surname"] = form_data["surname"]
        client["age"] = form_data["age"]
        client["country"] = form_data["country"]
        client["email"] = form_data["email"]
        
        client["username"] = form_data['username']
        client["password"] = form_data['password']
        
        functions.register_client(client)

    return render_template("Confirmed.html")
        
# Configuración y arranque de la aplicación web
app.run(host='localhost', port=5069, debug=True)