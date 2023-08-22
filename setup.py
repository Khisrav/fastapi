import mysql.connector

def execute_sql_from_file(filename, connection_params):
    try:
        connection = mysql.connector.connect(**connection_params)
        cursor = connection.cursor()

        with open(filename, 'r') as sql_file:
            sql_statements = sql_file.read()

        statements = sql_statements.split(';')

        for statement in statements:
            if statement.strip():
                cursor.execute(statement)

        connection.commit()
        print("SQL statements executed successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()

if __name__ == "__main__":
    sql_filename = "mysql.sql"
    db_params = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'fastapi'
    }
    execute_sql_from_file(sql_filename, db_params)
