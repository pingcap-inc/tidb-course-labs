from mysql.connector import connect
from mysql.connector import Error
from _mysql_connector import MySQLInterfaceError
import random
import time
import threading
import sys

def database_worker(thread_id):

    while True:
        try:

            conn = connect(
                database="test",
                host="<LB_DNS>",
                port=4000,
                user="root",
                password="",
            )
            cursor = conn.cursor(prepared=True)

            random_integer = random.randint(0, 10)
            random_id=random.randint(1, 10)
            query = "UPDATE test.users SET balance = " + str(random_integer) + " WHERE id = " + str(random_id) + ";"

            cursor.execute("BEGIN")
            cursor.execute(query)
            time.sleep(4)

            try:
                conn.commit()
                print(f"Thread {thread_id}: Committed. user {random_id} balance updated to: {random_integer}")
            except Error as e:
                print(f"Thread {thread_id}: Error during query execution: {e}")
            try:
                cursor.close()
                conn.close()
            except Error as e:
                pass

        except (Error, MySQLInterfaceError) as connect_err:
            print(f"Thread {thread_id}: Connection or execution error: {connect_err}")


def main():
    num_threads = 4

    print(f"Starting {num_threads} database worker threads...")

    # Create and start threads
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(
            target=database_worker,
            args=(i + 1,),
            daemon=True
        )
        threads.append(thread)
        thread.start()

        time.sleep(0.5)

    print(f"All {num_threads} threads started successfully!")

    try:
        # Keep the main thread alive - wait for threads to complete (they run indefinitely)
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print("\nReceived interrupt signal. Stopping all threads...")
        sys.exit(0)

if __name__ == "__main__":
    main()