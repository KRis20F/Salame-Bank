import functions, bbdd
from flask import Flask, render_template, request;

app = Flask(__name__)

# Declaración de rutas de la aplicación web
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/Login")
def login():
    return render_template("Login.html")

@app.route("/Signin")
def signin():
    return render_template("Signin.html")

# @app.route("/results",methods=('GET', 'POST'))
# def results():
#     if request.method == ('POST'):
#         form_data = request.form
#         user=form_data['usuario']
#         password=form_data['contrasena']
#         userData = Connect_user(user,password)

#         if userData == False:
#             return render_template("results.html",login=False)
#         else:
#             return render_template("results.html",login=True,userData=userData)

@app.route("/Sign-Account", methods=('GET', 'POST'))
def new_client():
    if request.method == 'POST':
        form_data = request.form
        name = form_data['name']
        surname = form_data['surname']
        age = form_data['age']
        country = form_data['country']
        functions.register_client(name, surname, age, country)

    return render_template("Sign-Account.html")

@app.route("/Confirmed", methods=('GET', 'POST'))
def new_account():
    if request.method == 'POST':
        form_data = request.form
        username = form_data['username']
        password = form_data['password']
        functions.register_account(username, password, 69000, False)

    return render_template("Confirmed.html")
        
# Configuración y arranque de la aplicación web
app.run(host='localhost', port=5069, debug=True)