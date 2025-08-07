from mysql.connector import connect
from mysql.connector import Error
from _mysql_connector import MySQLInterfaceError
import random
import time
import threading
import sys
from functools import wraps

def retry(max_attempts=2, delay=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except (Error, MySQLInterfaceError) as e:
                    if attempt == max_attempts - 1:  # Last attempt
                        print(f"All {max_attempts} attempts failed. Last error: {e}")
                        raise
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

@retry(max_attempts=2, delay=3)
def execute_database_operation(thread_id):

    conn = connect(
        database="test",
        host="<LB_DNS>",
        port=4000,
        user="root",
        password="",
    )
    cursor = conn.cursor(prepared=True)

    try:
        random_integer = random.randint(0, 10)
        random_id = random.randint(1, 10)
        query = "UPDATE test.users SET balance = " + str(random_integer) + " WHERE id = " + str(random_id) + ";"

        cursor.execute("BEGIN")
        cursor.execute(query)
        time.sleep(8)

        try:
            cursor.execute("COMMIT")
            print(f"Thread {thread_id}: Committed. user {random_id} balance updated to: {random_integer}")
        except Error as e:
            print(f"Thread {thread_id}: Error during query execution: {e}")
            raise

    finally:
        try:
            cursor.close()
            conn.close()
        except Error as e:
            pass

def database_worker(thread_id):
    """Worker function that continuously executes database operations"""
    while True:
        try:
            execute_database_operation(thread_id)
        except Exception as e:
            print(f"Thread {thread_id}: Operation failed after all retries: {e}")
            # Small delay before continuing to next iteration
            time.sleep(0.5)

def main():
    num_threads = 4

    print(f"Starting {num_threads} database worker threads...")

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