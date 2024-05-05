import mysql.connector

def connect_database():
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "salame_bank"
    )
    return conn

def register_client(client):
    database = connect_database()
    cursor = database.cursor()

    query = "INSERT INTO clients (name, surname, age, country) VALUES (%s, %s, %s, %s)"
    values = (client["name"], client["surname"], client["age"], client["country"])
    cursor.execute(query, values)

    print("cliente registrado")

    id_client = cursor.lastrowid

    register_account(client, id_client)

    database.commit()
    database.close()

def register_account(client, id_client):
    database = connect_database()
    cursor = database.cursor()

    query = "INSERT INTO accounts (id_client, username, password, currency, vip) VALUES (%s, %s, %s, %s, %s)"
    values = (id_client, client["username"], client["password"], 69000, False)
    cursor.execute(query, values)

    print("cuenta registrada")

    database.commit()
    database.close()

def connect_account(client):
    database = connect_database()
    cursor = database.cursor()

    query = """
        SELECT *
        FROM accounts
        WHERE username = %s AND password = %s;
    """
    values = (client["username"], client["password"])
    cursor.execute(query, values)

    result = cursor.fetchall()

    database.commit()
    database.close()

    if result:
        return True
    else:
        return False


def deposit(client, value):
    database = connect_database()
    cursor = database.cursor()

    query = """
        UPDATE accounts
        SET currency = currency + %s
        WHERE username = %s AND password = %s;
    """
    values = (value, client["username"], client["password"])
    cursor.execute(query, values)

    print("dinero ingresado")

    database.commit()
    database.close()

def withdraw(client, value):
    database = connect_database()
    cursor = database.cursor()

    query = """
        UPDATE accounts
        SET currency = currency - %s
        WHERE username = %s AND password = %s;
    """
    values = (value, client["username"], client["password"])
    cursor.execute(query, values)

    print("dinero retirado")

    database.commit()
    database.close()

def transfer(client, receiver, value):
    withdraw(client, value)
    database = connect_database()
    cursor = database.cursor()

    query = """
        UPDATE accounts
        SET currency = currency + %s
        WHERE username = %s;
    """
    values = (value, receiver)
    cursor.execute(query, values)

    print("dinero enviado")

    database.commit()
    database.close()