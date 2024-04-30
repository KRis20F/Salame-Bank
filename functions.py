import mysql.connector

def connect_database():
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "salame_bank"
    )
    return conn

def register_client(data):
    database = connect_database()
    cursor = database.cursor()

    query = "INSERT INTO clients (name, surname, age, country) VALUES (%s, %s, %s, %s)"
    values = (data["name"], data["surname"], data["age"], data["country"])
    cursor.execute(query, values)

    print("cliente registrado")

    id_client = cursor.lastrowid

    register_account(data, id_client)

    database.commit()
    database.close()

def register_account(data, id_client):
    database = connect_database()
    cursor = database.cursor()

    query = "INSERT INTO accounts (id_client, username, password, currency, vip) VALUES (%s, %s, %s, %s, %s)"
    values = (id_client, data["username"], data["password"], 69000, False)
    cursor.execute(query, values)

    print("cuenta registrada")

    database.commit()
    database.close()

def connect_account(user, password):
    pass

def deposit():
    pass

def withdraw():
    pass

def transfer():
    pass