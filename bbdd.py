import mysql.connector, functions

def connect_mysql():
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = ""
    )
    return db
def create_database():
    bd = connect_mysql()
    cursor = bd.cursor()

    # cursor.execute("DROP DATABASE IF EXISTS salame_bank;")
    cursor.execute("CREATE DATABASE salame_bank;")

    bd.commit()
    bd.close()

def create_tables():
    bd = functions.connect_database()
    cursor = bd.cursor()

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

    bd.commit()
    bd.close()
