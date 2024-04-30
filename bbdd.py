import mysql.connector, functions

def connect_mysql():
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = ""
    )
    return conn

def create_database():
    database = connect_mysql()
    cursor = database.cursor()

    # cursor.execute("DROP DATABASE IF EXISTS salame_bank;")
    cursor.execute("CREATE DATABASE salame_bank;")

    database.commit()
    database.close()

def create_tables():
    database = functions.connect_database()
    cursor = database.cursor()

    query = """
        CREATE TABLE clients (
            id_client INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(40),
            surname VARCHAR(60),
            age INT,
            country VARCHAR(60)
        )
    """
    cursor.execute(query)

    query = """
        CREATE TABLE accounts (
            id_account INT AUTO_INCREMENT PRIMARY KEY,
            id_client INT,
            username VARCHAR(20) UNIQUE,
            password VARCHAR(60),
            currency INT,
            vip BOOL,
            FOREIGN KEY (id_client) REFERENCES clients(id_client)
        )
    """
    cursor.execute(query)

    database.commit()
    database.close()
