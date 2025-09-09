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
                host="<HOST_MONITOR1_PRIVATE_IP>",
                port=6000,
                user="root",
                password="",
            )
            cursor = conn.cursor(prepared=True)

            # Get the actual TiDB server information
            cursor.execute("SELECT @@hostname as hostname, @@port as port, CONNECTION_ID() as connection_id")
            server_info = cursor.fetchone()
            hostname, port, connection_id = server_info

            # Extract IP address from hostname (format: ip-10-90-2-124.ap-northeast-1.compute.internal)
            if hostname.startswith('ip-'):
                ip_parts = hostname.split('.')[0].split('-')[1:]  # Split by '.' then by '-', skip 'ip'
                ip_address = '.'.join(ip_parts)
            else:
                ip_address = hostname  # Fallback to original hostname if format is unexpected

            random_integer = random.randint(0, 10)
            random_id=random.randint(1, 10)
            query = "UPDATE test.users SET balance = " + str(random_integer) + " WHERE id = " + str(random_id) + ";"

            cursor.execute("BEGIN")
            cursor.execute(query)
            time.sleep(4)

            try:
                cursor.execute("COMMIT")
                print(f"Thread {thread_id}: Connected to TiDB server {ip_address}:{port}. User {random_id} balance updated to: {random_integer}")
            except Error as e:
                print(f"Thread {thread_id}: Connected to TiDB server {ip_address}:{port}. Error during query execution: {e}")
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