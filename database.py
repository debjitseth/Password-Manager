import sqlite3

# Function to create a connection to the SQLite database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

# Function to create the passwords table if it doesn't exist
def create_table(conn):
    create_table_sql = """
        CREATE TABLE IF NOT EXISTS passwords (
            application TEXT PRIMARY KEY,
            username TEXT,
            password TEXT
        );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

# Function to insert a new password into the database
def insert_password(conn, username, application, password):
    sql = """
        INSERT INTO passwords(username, application, password)
        VALUES(?, ?, ?)
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (username, application, password))
        conn.commit()
        print("Password saved to database.")
        print("")
    except sqlite3.Error as e:
        print(e)

def add_password(conn, username, application, password):
    sql = """
        INSERT INTO passwords(username, application, password)
        VALUES(?, ?, ?)
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (username, application, password))
        conn.commit()
        print("Password saved to database.")
        print("")
    except sqlite3.Error as e:
        print(e)

def update_password(conn, application, password):
    sql = """
        UPDATE passwords 
        SET password = ? 
        WHERE application = ?
        """
    try:
        cursor = conn.cursor()
        cursor.execute(sql,(password,application))
        conn.commit()
        print("Password updated successfully.")
        print("")
    except sqlite3.Error as e:
        print(e)

        

def check_application_exists(conn, application):
    cursor = conn.cursor()
    cursor.execute("SELECT application FROM passwords WHERE application = ?", (application,))
    result = cursor.fetchone()
    return result is not None

def get_all_applications(conn):
    """
    Retrieve all application names from the database.
    """
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT application FROM passwords")
        rows = cursor.fetchall()
        applications = [row[0] for row in rows]
        return applications
    except sqlite3.Error as e:
        print(e)
        return []

#retrieving passwords
def get_password(conn, application):
    sql = """
        SELECT password
        FROM passwords
        WHERE application = ?
        """
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (application,))
        row = cursor.fetchone()
        if row:
            return row[0]  # Return the password from the fetched row
        else:
            return None  # Return None if no password is found
    except sqlite3.Error as e:
        print(e)
        return None

def delete_password(conn, application):
    sql = """
        DELETE FROM passwords
        WHERE application = ?
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (application,))
        conn.commit()
        print("Password deleted from database.")
        print("")
    except sqlite3.Error as e:
        print(e)
    