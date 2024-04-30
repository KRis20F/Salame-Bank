import mysql.connector

def connect_database():
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "salame_bank"
    )
    return conn

def register_client(name, surname, age, country):
    database = connect_database()
    cursor = database.cursor()

    query = "INSERT INTO clients (name, surname, age, country) VALUES (%s, %s, %s, %s)"
    values = (name, surname, age, country)
    cursor.execute(query, values)

    print("cliente registrado")

    database.commit()
    database.close()

def register_account(username, password, currency, vip):
    database = connect_database()
    cursor = database.cursor()

    query = "INSERT INTO accounts (username, password, currency, vip) VALUES (%s, %s, %s, %s)"
    values = (username, password, currency, vip)
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