import mysql.connector
from mysql.connector import Error
import time
from config.config import DATABASE_CONFIG, TEST_DATABASE_CONFIG
from contextlib import contextmanager
from app.logger import log_error
from utils.queue_utils import db_result_queue

class DatabaseConnectionError(Exception):
    """Custom exception for database connection errors"""
    pass

def get_db_connection(host, config_type="prod", max_retries=3000, retry_delay=1):
    """
    Get database connection with retry mechanism
    
    Args:
        host: TiDB server host address
        config_type: "prod" or "test" to select configuration
        max_retries: Maximum number of connection attempts
        retry_delay: Delay in seconds between retries
    """
    retries = 0
    last_error = None
    
    # Select configuration based on type
    if config_type == "test":
        config = TEST_DATABASE_CONFIG.copy()
    else:
        config = DATABASE_CONFIG.copy()
    
    # Set host in config
    config["host"] = host
    
    while retries < max_retries:
        try:
            conn = mysql.connector.connect(**config)
            
            # Test connection is alive
            cursor = conn.cursor()
            cursor.execute("SET SESSION MAX_EXECUTION_TIME=1000")
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            
            # Send recovery message if retry was successful
            if retries > 0:
                db_result_queue.put(('DB_RECOVERED', 'Database connection restored'))
            
            return conn
            
        except Error as err:
            last_error = err
            retries += 1
            
            if retries < max_retries:
                log_error(f"Database connection attempt {retries} failed: {err}")
                # Send retry message to queue
                retry_msg = f"Retry {retries}/{max_retries}: {str(err)}"
                db_result_queue.put(('DB_RETRY', retry_msg))
                time.sleep(retry_delay)
            
    raise DatabaseConnectionError(f"Failed to connect to database after {max_retries} attempts. Last error: {last_error}")

@contextmanager
def get_cursor(host, config_type="prod", max_retries=3, retry_delay=1):
    """
    Get database cursor with connection retry mechanism
    
    Args:
        host: TiDB server host address
        config_type: "prod" or "test" to select configuration
        max_retries: Maximum number of connection attempts
        retry_delay: Delay in seconds between retries
    """
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection(host, config_type, max_retries, retry_delay)
        cursor = conn.cursor(dictionary=True)
        
        # Enable automatic reconnection
        conn.ping(reconnect=True, attempts=3000, delay=1)
        
        yield cursor, conn
        conn.commit()
        
    except Error as e:
        if conn:
            conn.rollback()
        raise DatabaseConnectionError(f"Database operation failed: {str(e)}")
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
