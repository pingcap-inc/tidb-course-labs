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
            # Each thread creates its own connection
            conn = connect(
                database="test",
                host="<host_address>",
                port=4000,
                user="root",
                password="<your password>",
                ssl_verify_cert=True,
                ssl_verify_identity=True,
            )
            print(f"Thread {thread_id}: Connected to TiDB")
            cursor = conn.cursor(prepared=True)

            while True:
                random_integer = random.randint(0, 10)
                query = "UPDATE test.users SET balance = " + str(random_integer) + " WHERE id = 1;"

                time.sleep(0.5)
                try:
                    cursor.execute(query)
                    conn.commit()
                    print(f"Thread {thread_id}: Committed. Alice balance updated to: {random_integer}")
                except Error as e:
                    print(f"Thread {thread_id}: Error during query execution: {e}")
                    cursor.close()
                    conn.close()
                    break

        except (Error, MySQLInterfaceError) as connect_err:
            print(f"Thread {thread_id}: Connection error: {connect_err}")
            # Only close if cursor/conn exist
            try:
                cursor.close()
                conn.close()
            except:
                pass
            break

def main():
    num_threads = 5

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
    print("Press Ctrl+C to stop all threads...")

    try:
        # Keep the main thread alive - wait for threads to complete (they run indefinitely)
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print("\nReceived interrupt signal. Stopping all threads...")
        sys.exit(0)

if __name__ == "__main__":
    main()