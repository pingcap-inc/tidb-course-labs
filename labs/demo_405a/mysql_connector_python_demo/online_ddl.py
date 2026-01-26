import time
import sys
import argparse
import mysql.connector
from mysql.connector import errorcode
from demo_connection import get_connection


def setup_table(cursor, table_name):
    """Setup the test table"""
    # Disable TiDB metadata lock for online DDL operations
    try:
        cursor.execute("SET GLOBAL tidb_enable_metadata_lock = OFF")
        print("Disabled TiDB metadata lock for online DDL operations")
        
        # Show and print the variable status
        cursor.execute("SHOW VARIABLES LIKE 'tidb_enable_metadata_lock'")
        variable_status = cursor.fetchone()
        if variable_status:
            print(f"Current setting: {variable_status[0]} = {variable_status[1]}")
        else:
            print("Could not retrieve variable status")
    except mysql.connector.Error as err:
        print(f"Warning: Could not set tidb_enable_metadata_lock: {err}")
        print("Continuing with default settings...")
    
    # Drop table if it exists
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    
    # Create test table
    cursor.execute(f"""
        CREATE TABLE {table_name} (
            id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            k INT NOT NULL,
            c CHAR(120) NOT NULL,
            pad CHAR(60) NOT NULL,
            INDEX k_idx (k)
        )
    """)
    
    print(f"Created table {table_name}")


def insert_record(connection, cursor, insert_stmt, round_num):
    """Insert a record, handling schema mutation errors"""
    print(f"Inserting record {round_num}")
    
    try:
        # Attempt to execute the prepared statement
        cursor.execute(insert_stmt, (round_num, ))
        time.sleep(1)  # Simulate some work
        connection.commit()
        return True
    
    except mysql.connector.Error as err:
        # Check if it's error code 8028 (schema mutation)
        if err.errno == 8028:
            print("Schema mutation encountered, retrying...")
            retry_attempts = 0
            max_retries = 5
            backoff_time = 1  # Start with 1 second backoff
            while retry_attempts < max_retries:
                try:
                    time.sleep(backoff_time)
                    cursor.execute(insert_stmt, (round_num, ))
                    time.sleep(1)
                    connection.commit()
                    return True
                except mysql.connector.Error as retry_err:
                    if retry_err.errno == 8028:
                        retry_attempts += 1
                        backoff_time *= 2  # Exponential backoff
                        print(f"Retry {retry_attempts} failed: {retry_err}. Retrying in {backoff_time} seconds...")
                    else:
                        print(f"Retry failed with different error: {retry_err}")
                        return False
            print("Max retries reached. Moving to next record.")
            return False
        else:
            # Handle other MySQL errors
            print(f"Error: {err}")
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Check your username and password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(f"Error code: {err.errno}")
            return False


def run_insert_job(table_name="online_ddl_test"):
    """Run continuous insert job, handling online DDL operations"""
    try:
        # Connect to TiDB with auto-commit turned off
        with get_connection(autocommit=False) as connection:
            print(f"Connected to TiDB: {connection.user}@{connection.server_host}:{connection.server_port} using database {connection.database}")
            
            # Create a cursor
            with connection.cursor() as cursor:
                # Setup the test table
                setup_table(cursor, table_name)
                connection.commit()
                
                # SQL for inserting data (similar to Java example)
                insert_stmt = f"INSERT INTO {table_name} (k, c, pad) VALUES (%s, 'A', 'B')"
                
                # Run continuous insert loop
                round_num = 0
                while True:
                    success = insert_record(connection, cursor, insert_stmt, round_num)
                    if success:
                        round_num += 1
                    else:
                        # Pause briefly before retrying on failure
                        time.sleep(2)
    
    except KeyboardInterrupt:
        print("\nInsert job stopped by user")
    except mysql.connector.Error as err:
        print(f"Connection error: {err}")
        sys.exit(1)


def run_alter_table(table_name="online_ddl_test"):
    """Execute ALTER TABLE to add a column"""
    try:
        # Connect to TiDB with autocommit turned on explicitly for DDL operations
        with get_connection(autocommit=True) as connection:
            print(f"Connected to TiDB: {connection.user}@{connection.server_host}:{connection.server_port} using database {connection.database}")
            
            # Create a cursor
            with connection.cursor(buffered=True) as cursor:  # Use buffered cursor
                # Check if table exists
                try:
                    cursor.execute(f"SELECT 1 FROM {table_name} LIMIT 1")
                    # Explicitly consume the result set
                    cursor.fetchall()
                    print(f"Table {table_name} exists, proceeding with ALTER TABLE")
                except mysql.connector.Error as err:
                    print(f"Table {table_name} does not exist or cannot be accessed. Error: {err}")
                    print("Make sure to run the insert job first to create the table.")
                    return
                
                # Execute ALTER TABLE
                alter_stmt = f"ALTER TABLE {table_name} ADD COLUMN (ed VARCHAR(10) DEFAULT 'N/A')"
                print(f"Executing: {alter_stmt}")
                
                start_time = time.time()
                
                # Execute the statement without expecting results for DDL
                cursor.execute(alter_stmt)
                # DDL operations don't return results, but call fetchall() to be sure
                if cursor.with_rows:
                    cursor.fetchall()
                
                end_time = time.time()
                
                print(f"ALTER TABLE completed successfully in {end_time - start_time:.2f} seconds")
                
                # Verify the new column exists - this WILL have a result set we need to consume
                cursor.execute(f"DESCRIBE {table_name}")
                columns = cursor.fetchall()  # Important to consume this result set
                print("\nUpdated table structure:")
                for column in columns:
                    print(f"  {column[0]}: {column[1]}")
    
    except mysql.connector.Error as err:
        print(f"Error executing ALTER TABLE: {err}")
        print(f"Error code: {err.errno}")
        sys.exit(1)


def main():
    """Parse arguments and run the specified operation"""
    parser = argparse.ArgumentParser(description="TiDB Online DDL demonstration")
    
    # Create mutually exclusive group for operations
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--insert", action="store_true", help="Run the insert job")
    group.add_argument("--alter", action="store_true", help="Execute the ALTER TABLE command")
    
    # Optional table name argument
    parser.add_argument("table", nargs="?", default="online_ddl_test", 
                        help="Name of the table to use (default: online_ddl_test)")
    
    args = parser.parse_args()
    
    if args.insert:
        print(f"Starting insert job on table {args.table}")
        print("You can now run ALTER TABLE in another terminal with:")
        print(f"python online_ddl.py --alter {args.table}")
        run_insert_job(args.table)
    elif args.alter:
        print(f"Executing ALTER TABLE on {args.table}")
        run_alter_table(args.table)


if __name__ == "__main__":
    main()
