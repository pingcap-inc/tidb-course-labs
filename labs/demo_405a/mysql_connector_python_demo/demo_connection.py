import os

from dotenv import load_dotenv

import mysql.connector
from mysql.connector import MySQLConnection
from mysql.connector import errorcode


def get_connection(autocommit: bool = True) -> MySQLConnection:
    load_dotenv()
    db_conf = {
        "host": os.getenv("TIDB_HOST"),
        "port": int(os.getenv("TIDB_PORT")),
        "user": os.getenv("TIDB_USER"),
        "password": os.getenv("TIDB_PASSWORD"),
        "database": os.getenv("TIDB_DB_NAME"),
        "ssl_verify_cert": True,
        "ssl_verify_identity": True,
        "autocommit": autocommit,
        # mysql-connector-python will use C extension by default,
        # to make this example work on all platforms more easily,
        # we choose to use pure python implementation.
        "use_pure": True,
    }

    try:
        return mysql.connector.connect(**db_conf)
    except mysql.connector.Error as e:
        if e.errno == errorcode.ER_BAD_DB_ERROR:
            temp_db_conf = db_conf.copy()
            database = temp_db_conf["database"]
            del temp_db_conf["database"]
            with mysql.connector.connect(**temp_db_conf) as temp_conn:
                with temp_conn.cursor() as temp_cursor:
                    print(f"Create database {database}")
                    temp_cursor.execute(
                        f"CREATE DATABASE IF NOT EXISTS `{database}`"
                    )
            return mysql.connector.connect(**db_conf)
        else:
            raise e


if __name__ == "__main__":
    with get_connection() as conn:
        print(f"Connected to {conn.server_host}:{conn.server_port} as {conn.user} (Connection ID: {conn.connection_id})")
        print(f"The server is running {conn.get_server_info()}")