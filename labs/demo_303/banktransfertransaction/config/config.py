import os

# Get database host from environment variable or use default
DB_HOST = os.getenv('TIDB_HOST')

# Execution 
DATABASE_CONFIG = {
    "host": DB_HOST,
    "port": 4000,
    "user": "root",
    "database": "banking_system"
}

# Initiate db
TEST_DATABASE_CONFIG = {
    "host": DB_HOST,
    "port": 4000,
    "user": "root",
    "database": "test"
}

# Logger
LOG_CONFIG = {
    "filename": "bank_transfer.log",
    "format": "[%(asctime)s.%(msecs)03d] %(levelname)s: %(message)s",
    "datefmt": "%Y-%m-%d %H:%M:%S"
} 