from demo_connection import get_connection


with get_connection(autocommit=False) as connection:
    with connection.cursor(dictionary=True) as cursor:
        query_setup = "CREATE TABLE IF NOT EXISTS t1 (pk INT, name CHAR(30))"
        query_insert = "INSERT INTO t1 (pk, name) VALUES (%s, %s)"
        cursor.execute(query_setup)
        cursor.execute(query_insert, (1, "ABC"))
        connection.commit()

        print("1 row inserted into table t1 by positional placeholders")

