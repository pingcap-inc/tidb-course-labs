import time

from demo_connection import get_connection


def _setup(cursor):
    sql_drop_table = "DROP TABLE IF EXISTS t1_batchtest"
    sql_create_table = ("CREATE TABLE t1_batchtest (pk BIGINT PRIMARY KEY AUTO_RANDOM, name CHAR(30))")
    cursor.execute(sql_drop_table)
    cursor.execute(sql_create_table)


def _non_batch_style_insert(cursor, row_count):
    _setup(cursor)
    sql_insert = "INSERT INTO t1_batchtest (name) VALUES (%s)"
    b_time = time.time() * 1000
    for r in range(1, row_count + 1):
        cursor.execute(sql_insert, (r,))
    elapsed_time = time.time() * 1000 - b_time
    print("Non-Batch Inserting", row_count, "rows in", str(elapsed_time), "(ms).")


def _batch_style_insert(cursor, row_count):
    _setup(cursor)
    b_time = time.time() * 1000
    # Create a list of tuples for the values
    batch_values = [(str(r),) for r in range(1, row_count + 1)]
    # Use executemany for better performance and security
    cursor.executemany("INSERT INTO t1_batchtest (name) VALUES (%s)", batch_values)
    elapsed_time = time.time() * 1000 - b_time
    print("Batch Inserting", row_count, "rows in", str(elapsed_time), "(ms).")


def _check_result(cursor):
    query = "SELECT count(*) FROM t1_batchtest"
    cursor.execute(query)
    for (row_count,) in cursor:
        print(f"Total rows in t1_batchtest table: {row_count}.")


if __name__ == "__main__":
    with get_connection() as connection:
        print(f"Connected to TiDB: {connection.user}@{connection.server_host}:{connection.server_port}")
        with connection.cursor() as cursor:
            # Batching
            _batch_style_insert(cursor, 1000)
            connection.commit()
            _check_result(cursor)

            # Non-Batching
            _non_batch_style_insert(cursor, 1000)
            connection.commit()
            _check_result(cursor)
