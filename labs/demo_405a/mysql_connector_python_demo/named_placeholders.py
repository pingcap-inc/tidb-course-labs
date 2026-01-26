from demo_connection import get_connection


with get_connection(autocommit=False) as connection:
    with connection.cursor(dictionary=True) as cursor:
        query_setup = "CREATE TABLE IF NOT EXISTS t1 (pk INT, name CHAR(30))"
        query_insert = "INSERT INTO t1 (pk, name) VALUES (%(pk)s, %(name)s)"
        cursor.execute(query_setup)
        cursor.execute(query_insert, {"pk": 2, "name": "DEF"})
        connection.commit()

        print("1 row inserted into table t1 by named placeholders")

