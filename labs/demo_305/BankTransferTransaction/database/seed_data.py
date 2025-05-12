import os
import sys
import random
from decimal import Decimal
import argparse

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from database.db_connection import get_cursor

def seed_accounts(cursor, num_accounts=100):
    """Initialize account data"""
    print("Starting account initialization...")
    
    # Prepare batch insert data
    accounts_data = []
    for i in range(num_accounts):
        account = (
            f"user_{i+1:02d}",  # account_name
            Decimal(str(random.randrange(10, 101) * 100)).quantize(Decimal('0.00'))  # balance
        )
        accounts_data.append(account)
    
    # Batch insert account data
    cursor.executemany(
        """
        INSERT INTO banking_system.accounts (account_name, balance)
        VALUES (%s, %s)
        """,
        accounts_data
    )
    
    print(f"Successfully created {num_accounts} accounts")

def seed_transactions(cursor, num_transactions=100):
    """Initialize transaction records"""
    print("Starting transaction initialization...")
    
    # Get all account IDs
    cursor.execute("SELECT account_id, balance FROM banking_system.accounts")
    accounts = {row['account_id']: row['balance'] for row in cursor.fetchall()}
    
    if len(accounts) < 2:
        print("Insufficient accounts to create transactions")
        return
    
    # Prepare batch insert data
    transactions_data = []
    for _ in range(num_transactions):
        # Randomly select sender and receiver
        sender_id, receiver_id = random.sample(list(accounts.keys()), 2)
        amount = Decimal(str(random.randrange(1, 11) * 100)).quantize(Decimal('0.00'))
        status = random.choice(['SUCCESS', 'FAILED'])
        
        # Get balances
        sender_balance = accounts[sender_id]
        receiver_balance = accounts[receiver_id]
        
        # Calculate after balances based on status
        if status == 'SUCCESS':
            sender_balance_after = sender_balance - amount
            receiver_balance_after = receiver_balance + amount
            note = None
        else:
            sender_balance_after = sender_balance
            receiver_balance_after = receiver_balance
            note = "Insufficient balance"
        
        transaction = (
            sender_id,  # sender_id
            receiver_id,  # receiver_id
            amount,  # amount
            status,  # status
            sender_balance,  # sender_balance_before
            sender_balance_after,  # sender_balance_after
            receiver_balance,  # receiver_balance_before
            receiver_balance_after,  # receiver_balance_after
            note  # note
        )
        transactions_data.append(transaction)
    
    # Batch insert transaction records
    cursor.executemany(
        """
        INSERT INTO banking_system.transactions 
        (sender_id, receiver_id, amount, status, 
         sender_balance_before, sender_balance_after,
         receiver_balance_before, receiver_balance_after,
         note)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        transactions_data
    )
    
    print(f"Successfully created {num_transactions} transaction records")

def main():
    parser = argparse.ArgumentParser(description='Seed database with test data')
    parser.add_argument('--host', type=str, required=True,
                        help='TiDB server host address')
    args = parser.parse_args()

    print(f"\nConnecting to TiDB server at {args.host}...")
    
    try:
        with get_cursor(args.host) as (cursor, conn):
            # Check if database exists
            cursor.execute("USE banking_system")
            
            # Empty tables in the correct order (first delete tables with foreign key constraints)
            cursor.execute("DELETE FROM banking_system.transactions")
            cursor.execute("DELETE FROM banking_system.accounts")
            
            # Initialize data
            seed_accounts(cursor)
            # seed_transactions(cursor)
            
            print("Data initialization completed!")
            
            # Display some statistics
            cursor.execute("SELECT COUNT(*) as count FROM banking_system.accounts")
            accounts_count = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM banking_system.transactions")
            transactions_count = cursor.fetchone()['count']
            
            print(f"\nStatistics:")
            print(f"Total accounts: {accounts_count}")
            print(f"Total transaction records: {transactions_count}")
            
    except Exception as e:
        print(f"Data initialization failed: {str(e)}")

if __name__ == "__main__":
    main() 