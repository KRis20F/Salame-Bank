
import mysql.connector
from flask import Flask, render_template, request;

def connect_database():
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "clients"
    )
    return db

def connect_user(user, password):
    pass

def register_user(user, password, name, surname, age):
    bd=connect_database()
    cursor=bd.cursor()

    query = f"INSERT INTO clients\
        VALUES(%s,%s,%s,%s,%s,%s,%s);"
    values = (user, password, name, surname, age)
    cursor.execute(query, values)

    bd.commit()
    bd.close()

def deposit():
    pass

def withdraw():
    pass

def transfer():
    pass

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
#         formData = request.form
#         user=formData['usuario']
#         password=formData['contrasena']
#         userData = Connect_user(user,password)

#         if userData == False:
#             return render_template("results.html",login=False)
#         else:
#             return render_template("results.html",login=True,userData=userData)
# Configuración y arranque de la aplicación web
import mysql.connector
from flask import Flask, render_template, request;

def connect_database():
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "clients"
    )
    return db

def connect_user(user, password):
    pass

def register_user(user, password, name, surname, age):
    bd=connect_database()
    cursor=bd.cursor()

    query = f"INSERT INTO clients\
        VALUES(%s,%s,%s,%s,%s,%s,%s);"
    values = (user, password, name, surname, age)
    cursor.execute(query, values)

    bd.commit()
    bd.close()

def deposit():
    pass

def withdraw():
    pass

def transfer():
    pass

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
#         formData = request.form
#         user=formData['usuario']
#         password=formData['contrasena']
#         userData = Connect_user(user,password)

#         if userData == False:
#             return render_template("results.html",login=False)
#         else:
#             return render_template("results.html",login=True,userData=userData)

# @app.route("/newUser", methods=('GET', 'POST'))
# def newUser():
#     if request.method == 'POST':
#         formData = request.form
#         user = formData['usuario']
#         password = formData['contrasena']
#         name = formData['name']
#         surname1 = formData['surname1']
#         surname2 = formData['surname2']
#         age = formData['age']
#         genre = formData['genre']
#         register_user(user, password, name, surname1, surname2, age, genre)

#     return render_template("newUser.html")
        
# Configuración y arranque de la aplicación web

app.run(host='localhost', port=5069, debug=True)