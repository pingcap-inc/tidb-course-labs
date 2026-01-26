from demo_connection import get_connection
import threading

def setup():
    # Initialize the database
    conn = get_connection(autocommit=False)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS users;")
    cur.execute("CREATE TABLE users (id BIGINT, name VARCHAR(20));")
    cur.execute("INSERT INTO users VALUES (1, 'Tom');")
    conn.commit()
    cur.close()
    conn.close()

def thread1_task():
    conn1 = get_connection(autocommit=False)
    cur1 = conn1.cursor(dictionary=True)
    cur1.execute("BEGIN PESSIMISTIC;")
    print("[Thread1] BEGIN PESSIMISTIC", flush=True)

    # notify thread2 to begin transaction
    thread1_begin.set()

    # update and hold lock
    cur1.execute("UPDATE users SET name = 'conn1' WHERE id = 1;")
    print("[Thread1] UPDATED row → name='conn1'", flush=True)

    # notify thread2 to begin transaction
    thread1_updated.set()

    # wait thread2 to attempt update (blocked)
    thread2_ready.wait()

    cur1.execute("COMMIT;")
    print("[Thread1] COMMITTED", flush=True)

    cur1.close()
    conn1.close()

def thread2_task():
    conn2 = get_connection(autocommit=False)
    cur2 = conn2.cursor(dictionary=True)

    # wait thread1 to complete BEGIN
    thread1_begin.wait()

    cur2.execute("BEGIN PESSIMISTIC;")
    print("[Thread2] BEGIN PESSIMISTIC", flush=True)

    # wait thread1 to update and hold lock
    thread1_updated.wait()

    # notify thread1 that I will attempt UPDATE
    thread2_ready.set()
    print("[Thread2] attempting UPDATE (will block)...", flush=True)

    # this line will be blocked until thread1 COMMIT release row lock
    cur2.execute("UPDATE users SET name = 'conn2' WHERE id = 1;")
    print("[Thread2] UPDATED row → name='conn2'", flush=True)

    cur2.execute("COMMIT;")
    print("[Thread2] COMMITTED", flush=True)

    cur2.close()
    conn2.close()

def print_result():
    conn = get_connection(autocommit=False)
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users;")
    print("Update Result: name is changed to", cur.fetchall()[0].get('name'))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    # event for thread synchronization
    thread1_begin   = threading.Event()
    thread1_updated = threading.Event()
    thread2_ready   = threading.Event()
    setup()
    t1 = threading.Thread(target=thread1_task)
    t2 = threading.Thread(target=thread2_task)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print_result()
