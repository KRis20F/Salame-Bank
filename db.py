import mysql.connector, functions

def connect_mysql(): # Conexion al mysql
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = ""
    )
    return conn

def create_database(): # Genera la base de datos si no existe
    try:
        database = connect_mysql()
        cursor = database.cursor()

        cursor.execute("SHOW DATABASES LIKE 'salame_bank'")
        is_created = cursor.fetchone()

        if not is_created:
            cursor.execute("CREATE DATABASE salame_bank;")
            create_tables()

        database.commit()
        database.close()

    except Exception as error:
        print("Error detected:", error)

def create_tables(): # Genera las tablas de la base de datos
    database = functions.connect_database()
    cursor = database.cursor()

    clients_table = """
        CREATE TABLE clients (
            id_client INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(40),
            surname VARCHAR(60),
            age INT,
            country VARCHAR(60),
            email VARCHAR(80) UNIQUE
        );
    """

    accounts_table = """
        CREATE TABLE accounts (
            id_account INT AUTO_INCREMENT PRIMARY KEY,
            id_client INT,
            username VARCHAR(20) UNIQUE,
            password VARCHAR(60),
            currency INT,
            IBAN VARCHAR(30),
            FOREIGN KEY (id_client) REFERENCES clients(id_client)
        );
    """

    transactions_table = """
        CREATE TABLE transactions (
            id_transactions INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(20),
            old_currency INT,
            new_currency INT,
            date DATE,
            time TIME,
            balance INT,
            type VARCHAR(20)
        );
    """

    cursor.execute(clients_table)
    cursor.execute(accounts_table)
    cursor.execute(transactions_table)

    create_triggers(cursor)

    database.commit()
    database.close()

def create_triggers(cursor): # Genera los triggers de la base de datos
    check_trigger = """ 
        CREATE TRIGGER check_transaction 
        BEFORE UPDATE ON accounts FOR EACH ROW
        BEGIN
            IF NEW.currency < 0 THEN
                SIGNAL SQLSTATE '45000' 
                SET MESSAGE_TEXT = "NEGATIVE BALANCE ERROR";
            END IF;
        END;
    """

    register_trigger = """
        CREATE TRIGGER register_transaction 
        AFTER UPDATE ON accounts FOR EACH ROW
        BEGIN
            DECLARE v_balance INT;
            DECLARE v_type VARCHAR(20);

            SET v_balance = NEW.currency - OLD.currency;

            IF (SELECT COUNT(*) FROM transactions WHERE date = CURRENT_DATE AND time = CURRENT_TIME) > 0 THEN
                SET v_type = "transfer";
                UPDATE transactions 
                SET type = "transfer" 
                WHERE date = CURRENT_DATE AND time = CURRENT_TIME;
            ELSEIF v_balance > 0 THEN
                SET v_type = "deposit";
            ELSE
                SET v_type = "withdraw";
            END IF;

            INSERT INTO transactions (username, old_currency, new_currency, date, time, balance, type)
            VALUES (NEW.username, OLD.currency, NEW.currency, CURRENT_DATE, CURRENT_TIME, v_balance, v_type);
        END;
    """

    cursor.execute(check_trigger) # Se encarga de que tu cuenta no pueda tener numeros negativos
    cursor.execute(register_trigger) # Se encarga de guardar el registro de todas las operaciones realizadas
