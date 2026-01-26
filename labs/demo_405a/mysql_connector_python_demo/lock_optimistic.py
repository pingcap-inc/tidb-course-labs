from demo_connection import get_connection
import threading
import mysql.connector
import sys

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
    cur1.execute("BEGIN OPTIMISTIC;")
    print("[Thread1] BEGIN OPTIMISTIC", flush=True)

    # update 
    cur1.execute("UPDATE users SET name = 'conn1' WHERE id = 1;")
    print("[Thread1] UPDATED row → name='conn1'", flush=True)

    # thread1 try to commit.
    # error(s) will be raised if there is a conflict
    try:
        cur1.execute("UPDATE users SET name = 'conn1' WHERE id = 1;")
        print("[Thread1] UPDATED row → name='conn1'", flush=True)
        print("[Thread1] Try to commit", flush=True)
        cur1.execute("COMMIT;")
        print("[Thread1] Commit Successful", flush=True)

    except mysql.connector.Error as err:
        print("[Thread1] Conflict occurs: {}".format(err), flush=True)
        print("[Thread1] Retry", flush=True)
        try:
            cur1.execute("BEGIN OPTIMISTIC;")
            print("[Thread1 retry] BEGIN OPTIMISTIC", flush=True)

            cur1.execute("UPDATE users SET name = 'conn1' WHERE id = 1;")
            print("[Thread1 retry] UPDATED row → name='conn1'", flush=True)

            cur1.execute("COMMIT;")
            print("[Thread1 retry] Commit successful", flush=True)

        except mysql.connector.Error as err:
            print("[Thread1 retry] Conflict occurs: {}".format(err), flush=True)

    cur1.close()
    conn1.close()

def thread2_task():
    conn2 = get_connection(autocommit=False)
    cur2 = conn2.cursor(dictionary=True)

    cur2.execute("BEGIN OPTIMISTIC;")
    print("[Thread2] BEGIN OPTIMISTIC", flush=True)

    # thread2 try to commit.
    # error(s) will be raised if there is a conflict
    try:
        cur2.execute("UPDATE users SET name = 'conn2' WHERE id = 1;")
        print("[Thread2] UPDATED row → name='conn2'", flush=True)
        print("[Thread2] Try to commit", flush=True)
        cur2.execute("COMMIT;")
        print("[Thread2] Commit Successful", flush=True)
    
    except mysql.connector.Error as err:
        print("[Thread2] Conflict occurs: {}".format(err), flush=True)
        print("[Thread2] Retry", flush=True)
        try:
            cur2.execute("BEGIN OPTIMISTIC;")
            print("[Thread2 retry] BEGIN OPTIMISTIC", flush=True)

            cur2.execute("UPDATE users SET name = 'conn2' WHERE id = 1;")
            print("[Thread2 retry] UPDATED row → name='conn2'", flush=True)

            cur2.execute("COMMIT;")
            print("[Thread2 retry] Commit successful", flush=True)

        except mysql.connector.Error as err:
            print("[Thread2 retry] Conflict occurs: {}".format(err), flush=True)

    cur2.close()
    conn2.close()

def print_result():
    conn = get_connection(autocommit=False)
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users;")
    print("Update Result: name is changed to", cur.fetchall()[0].get('name'), flush=True)
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    setup()
    t1 = threading.Thread(target=thread1_task)
    t2 = threading.Thread(target=thread2_task)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print_result()