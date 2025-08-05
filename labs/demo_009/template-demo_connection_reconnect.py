from mysql.connector import connect
from mysql.connector import Error
from _mysql_connector import MySQLInterfaceError
import random
import time

if __name__ == "__main__":

    while True:
        try:
            conn = connect(
                database="test",
                host="<HOST_DB2_PRIVATE_IP>",
                port=4000,
                user="root",
                password="",
            )
            print("Connected to TiDB:")
            cursor = conn.cursor(prepared=True)

            while True:
                random_integer = random.randint(0, 10)
                query = "UPDATE test.users SET balance = " + str(random_integer) + " WHERE id = 2;"

                time.sleep(0.5)
                try:
                    cursor.execute(query)
                    conn.commit()
                    print("Committed. Bob's balance updated to: ", random_integer)

                except Error as e:
                    print("Error during query execution:", e)
                    cursor.close()
                    conn.close()
                    break

        except (Error, MySQLInterfaceError) as connect_err:
            print("Connection error:", connect_err)

            try:
                conn = connect(
                    database="test",
                    host="<HOST_DB1_PRIVATE_IP>",
                    port=4000,
                    user="root",
                    password="",
                )
                print("Connected to TiDB again:")
                cursor = conn.cursor(prepared=True)

                while True:
                    random_integer = random.randint(0, 10)
                    query = "UPDATE test.users SET balance = " + str(random_integer) + " WHERE id = 1;"

                    time.sleep(0.5)
                    try:
                        cursor.execute(query)
                        conn.commit()
                        print("Committed. Bob's balance updated to: ", random_integer)

                    except Error as e:
                        print("Error during query execution:", e)
                        cursor.close()
                        conn.close()
                        break
            except:
                pass
            break
