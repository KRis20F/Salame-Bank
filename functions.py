import mysql.connector

def connect_database():
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "salame_bank"
    )
    return db

def register_client(name, surname, age, country):
    bd = connect_database()
    cursor = bd.cursor()

    query = f"INSERT INTO clients\
        VALUES(%s, %s, %s, %s);"
    values = (name, surname, age, country)
    cursor.execute(query, values)

    bd.commit()
    bd.close()

def register_account(username, password, currency, vip):
    bd = connect_database()
    cursor = bd.cursor()

    query = f"INSERT INTO accounts\
        VALUES(%s, %s, %s, %s);"
    values = (username, password, currency, vip)
    cursor.execute(query, values)

    bd.commit()
    bd.close()

def connect_account(user, password):
    pass

def deposit():
    pass

def withdraw():
    pass

def transfer():
    pass