import pypyodbc as odbc


def database_connection():
    DRIVER_NAME = 'ODBC Driver 17 for SQL Server'  
    SERVER_NAME = 'DESKTOP-DKRJMDR\SQLEXPRESS'
    DATABASE_NAME = 'new'
    connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trusted_Connection=yes;
    """
    
    connection = odbc.connect(connection_string)
    return connection

def fetch_data_from_database(connection):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM books")
    data_from_database = cursor.fetchall()

    cursor.close()

    return data_from_database

def fetch_year_from_database(connection):
    cursor = connection.cursor()

    cursor.execute("SELECT year FROM books")
    year_from_database = cursor.fetchall()

    cursor.close()

    return year_from_database

def delete_book(connection, book_id):
    cursor = connection.cursor()

    delete_query = f"DELETE FROM books WHERE id = {book_id}"
    cursor.execute(delete_query)

    connection.commit()

    cursor.close()

def insert_book(connection, title, author, year, genre):
    cursor = connection.cursor()

    insert_query = f"INSERT INTO books (Title, Author, Pub_Year , Genre) VALUES ('{title}', '{author}', '{year}', '{genre}')"
    cursor.execute(insert_query)

    connection.commit()

    cursor.close()

def update_book(connection, book_id, title, author, year, genre):
    cursor = connection.cursor()

    update_query = f"UPDATE books SET title = '{title}', author = '{author}', year = '{year}', genre = '{genre}' WHERE id = {book_id}"
    cursor.execute(update_query)

    connection.commit()

    cursor.close()

def get_item(connection, book_id):
    cursor = connection.cursor()

    select_query = f"SELECT * FROM books WHERE id = {book_id}"
    cursor.execute(select_query)
    data_from_database = cursor.fetchall()

    cursor.close()
    return data_from_database

