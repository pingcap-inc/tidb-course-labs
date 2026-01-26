from demo_connection import get_connection


with get_connection() as connection:
    with connection.cursor(dictionary=True) as cursor:
        query = "SELECT pk, name FROM t1 WHERE pk between %s and %s"
        start_idx = 1
        end_idx = 10
        cursor.execute(query, (start_idx, end_idx))
        result_tuple = cursor.fetchall()

        for row in result_tuple:
            print(f"PK of {row['name']} is {row['pk']}")
