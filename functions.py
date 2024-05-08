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
    try:
        database = connect_database()
        cursor = database.cursor()

        query = "INSERT INTO clients (name, surname, age, country, email) VALUES (%s, %s, %s, %s, %s)"
        values = (client["name"], client["surname"], client["age"], client["country"], client["email"])
        cursor.execute(query, values)

        print("cliente registrado")

        id_client = cursor.lastrowid

        register_account(cursor, client, id_client)

        database.commit()
        database.close()

    except Exception as error:
        print("Error detected:", error)

def register_account(cursor, client, id_client):
    query = "INSERT INTO accounts (id_client, username, password, currency) VALUES (%s, %s, %s, %s)"
    values = (id_client, client["username"], client["password"], 69000)
    cursor.execute(query, values)

    print("cuenta registrada")

def connect_account(client):
    client_info = {}

    try:
        database = connect_database()
        cursor = database.cursor()

        client_info = get_account(client, client_info, cursor)
        client_info = get_client(client, client_info, cursor)

        database.commit()
        database.close()
    
    except Exception as error:
        print("Error detected:", error)
        client_info = error
    
    finally:
        return client_info

def get_account(client, info, cursor):
    query = """
        SELECT *
        FROM accounts
        WHERE username = %s AND password = %s;
    """
    values = (client["username"], client["password"])
    cursor.execute(query, values)

    account_info = cursor.fetchall()

    info["username"] = account_info[0][2]
    info["password"] = account_info[0][3]
    info["currency"] = account_info[0][4]

    return info

def get_client(client, info, cursor):
    query = """
        SELECT *
        FROM clients
        INNER JOIN accounts ON clients.id_client = accounts.id_client
        WHERE accounts.username = %s AND accounts.password = %s;
    """
    values = (client["username"], client["password"])
    cursor.execute(query, values)

    account_info = cursor.fetchall()

    info["name"] = account_info[0][1]

    return info

def deposit(client, value):
    try:
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

        return True

    except Exception as error:
        print("Error detected:", error)
        return False


def withdraw(client, value):
    try:
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

        return True
    
    except Exception as error:
        print("Error detected:", error)
        return False

def transfer(client, receiver, value):
    try:
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

        return True
    
    except Exception as error:
        print("Error detected:", error)
        return False