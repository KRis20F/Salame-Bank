import mysql.connector, random , string

def connect_database(): # Conexion a la base de datos
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "salame_bank"
    )
    return conn

def register_client(client): # Guarda los datos del usuario a la base de datos
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

def register_account(cursor, client, id_client): # Guarda los datos de la cuenta del usuario a la base de datos
    query = "INSERT INTO accounts (id_client, username, password, currency, IBAN) VALUES (%s, %s, %s, %s, %s)"
    values = (id_client, client["username"] ,client["password"] ,0 ,create_IBAN())
    cursor.execute(query, values)

    print("cuenta registrada")

def connect_account(client): # Devuelve datos del usuario
    client_info = {}

    try:
        database = connect_database()
        cursor = database.cursor()

        client_info = get_account(client, client_info, cursor)
        client_info = get_client(client, client_info, cursor)

        database.commit()
        database.close()
    
    except TypeError as error:
        print("Error detectado:", error)
        client_info = "Datos incorrectos, intentalo de nuevo"
    
    except Exception as error:
        print("Error detectado:", error)
        client_info = "Error de conexión, intentalo más tarde"
    
    finally:
        return client_info

def get_account(client, info, cursor): # Busca y guarda los datos de la cuenta del usuario
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

def get_client(client, info, cursor): # Busca y guarda los datos del usuario
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

def check_transactions(client): # Busca en la tabla transactions las operaciones realizadas por el usuario
    try:
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
        
        database.commit()
        database.close()

        return account_info
    
    except Exception as error:
        print("Error detected:", error)
    
        return error

def deposit(client, password, value): # Gestiona la funcion de depositar dinero
    try:
        if int(value) > 0 and password == client["password"]:
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

def withdraw(client, password, value): # Gestiona la funcion de retirar dinero
    try:
        if int(value) > 0 and password == client["password"]:
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
        
        else:
            return False
    
    except Exception as error:
        print("Error detected:", error)
        
        return False

def transfer(client, receiver, password, value): # Gestiona la funcion de enviar dinero
    try:
        if int(value) > 0 and password == client["password"] and client["username"] != receiver:
            database = connect_database()
            cursor = database.cursor()

            is_active = check_user(cursor, receiver)

            if is_active:
                withdraw_query = """
                    UPDATE accounts
                    SET currency = currency - %s
                    WHERE username = %s AND password = %s;
                """
                deposit_query = """
                    UPDATE accounts
                    SET currency = currency + %s
                    WHERE username = %s;
                """

                values = (value, client["username"], password)
                cursor.execute(withdraw_query, values)

                values = (value, receiver)
                cursor.execute(deposit_query, values)

                print("dinero enviado")

                database.commit()
                database.close()

                return True
        
        return False
    
    except Exception as error:
        print("Error detected:", error)

        return False
    
def check_user(cursor, username):
    query = """
        SELECT *
        FROM accounts
        WHERE username = %s;
    """
    values = (username,)
    cursor.execute(query, values)

    client = cursor.fetchone()

    if not client:
        return False
    else:
        return True
