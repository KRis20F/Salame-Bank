import mysql.connector, random , string

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

        return True

    except Exception as error:
        print("Error detected:", error)
        
        return False

def register_account(cursor, client, id_client):
    query = "INSERT INTO accounts (id_client, username, password, currency, IBAN) VALUES (%s, %s, %s, %s, %s)"
    values = (id_client, client["username"], client["password"], 69000 , create_IBAN())
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
    
    except IndexError as index_error:
        print("Índice fuera de límites:", index_error)
        client_info = "Datos incorrectos, intentalo de nuevo"
    
    except Exception as error:
        print("Error detectado:", error)
        client_info = "Error de conexión, intentalo más tarde"
    
    finally:
        return client_info

def get_account(client, info, cursor):
    query = """
        SELECT id_client, username, password, currency, IBAN
        FROM accounts
        WHERE username = %s AND password = %s;
    """
    values = (client["username"], client["password"])
    cursor.execute(query, values)

    account_info = cursor.fetchone()

    info["id_client"] = account_info[0]
    info["username"] = account_info[1]
    info["password"] = account_info[2]
    info["currency"] = account_info[3]
    info["IBAN"] = account_info[4]

    return info

def get_client(client, info, cursor):
    query = """
        SELECT name , surname, age, country, email
        FROM clients
        INNER JOIN accounts ON clients.id_client = accounts.id_client
        WHERE accounts.username = %s AND accounts.password = %s;
    """
    values = (client["username"], client["password"])
    cursor.execute(query, values)

    account_info = cursor.fetchone()

    info["name"] = account_info[0]
    info["surname"] = account_info[1]
    info["age"] = account_info[2]
    info["country"] = account_info[3]
    info["email"] = account_info[4]

    return info

def create_IBAN():
    iban_prefix = 'ES' 
    iban_suffix = ''.join(random.choices(string.digits, k=10))
    new_iban = iban_prefix + iban_suffix

    return new_iban

def deposit(client, password, value):
    try:
        if client["password"] == password:
            database = connect_database()
            cursor = database.cursor()

            query = """
                UPDATE accounts
                SET currency = currency + %s
                WHERE username = %s AND password = %s;
            """
            values = (value, client["username"], password)
            cursor.execute(query, values)

            print("dinero ingresado")

            database.commit()
            database.close()

            return True
        else:
            return False

    except Exception as error:
        print("Error detected:", error)

        return False

def withdraw(client, password, value):
    try:
        database = connect_database()
        cursor = database.cursor()

        query = """
            UPDATE accounts
            SET currency = currency - %s
            WHERE username = %s AND password = %s;
        """
        values = (value, client["username"], password)
        cursor.execute(query, values)

        print("dinero retirado")

        database.commit()
        database.close()

        return True
    
    except Exception as error:
        print("Error detected:", error)

        return False

def transfer(client, receiver, password, value):
    try:
        withdraw(client, password, value)
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
    
def check_transactions(client):
    database = connect_database()
    cursor = database.cursor()

    query = """
        SELECT date , time , balance, type
        FROM transactions
        WHERE username = %s;
    """
    values = (client["username"],)
    cursor.execute(query, values)
    
    account_info = cursor.fetchall()
    
    print(account_info)
    
    database.commit()
    database.close()
    
    return account_info
    
    
    