from pymysql_demo.demo_connection import get_connection


with get_connection() as connection:
    with connection.cursor() as cursor:  # PyMySQL defaults to dict cursor from our connection setup
        query = "SELECT pk, name FROM t1 WHERE pk between %s and %s"
        start_idx = 1
        end_idx = 10
        cursor.execute(query, (start_idx, end_idx))

        row = cursor.fetchone()
        while row is not None:
            print(f"PK of {row['name']} is {row['pk']}")
            # You need to consume all the results
            row = cursor.fetchone() 