from decimal import Decimal
from app.logger import log_transaction, log_error

def transfer_amount(sender_id, receiver_id, amount, cursor, conn, elapsed_seconds=0):
    try:
        # Check the balance of sender
        cursor.execute(
            "SELECT account_id, balance FROM accounts WHERE account_id IN (%s, %s) FOR UPDATE",
            (sender_id, receiver_id)
        )
        accounts = {row['account_id']: row['balance'] for row in cursor.fetchall()}
        
        sender_balance_before = accounts.get(sender_id, 0)
        receiver_balance_before = accounts.get(receiver_id, 0)
        
        if not sender_balance_before or sender_balance_before < amount:
            log_transaction(
                sender_id, receiver_id, amount, "FAILED",
                sender_balance_before, receiver_balance_before,
                sender_balance_before, receiver_balance_before,
                "Insufficient balance",
                elapsed_seconds
            )
            # Insert failed transaction record
            cursor.execute("""
                INSERT INTO transactions 
                (sender_id, receiver_id, amount, status,
                 sender_balance_before, sender_balance_after,
                 receiver_balance_before, receiver_balance_after,
                 note)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                sender_id, receiver_id, amount, "FAILED",
                sender_balance_before, sender_balance_before,
                receiver_balance_before, receiver_balance_before,
                "Insufficient balance"
            ))
            conn.commit()
            return False, "Insufficient balance"
            
        # Update balance
        cursor.execute(
            "UPDATE accounts SET balance = balance - %s WHERE account_id = %s",
            (amount, sender_id)
        )
        cursor.execute(
            "UPDATE accounts SET balance = balance + %s WHERE account_id = %s",
            (amount, receiver_id)
        )
        
        # Get the balance after transfer
        cursor.execute(
            "SELECT account_id, balance FROM accounts WHERE account_id IN (%s, %s)",
            (sender_id, receiver_id)
        )
        updated_accounts = {row['account_id']: row['balance'] for row in cursor.fetchall()}
        
        sender_balance_after = updated_accounts.get(sender_id)
        receiver_balance_after = updated_accounts.get(receiver_id)
        
        # Record transaction
        cursor.execute("""
            INSERT INTO transactions 
            (sender_id, receiver_id, amount, status,
             sender_balance_before, sender_balance_after,
             receiver_balance_before, receiver_balance_after,
             note)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            sender_id, receiver_id, amount, "SUCCESS",
            sender_balance_before, sender_balance_after,
            receiver_balance_before, receiver_balance_after,
            None
        ))
        
        log_transaction(
            sender_id, receiver_id, amount, "SUCCESS",
            sender_balance_before, receiver_balance_before,
            sender_balance_after, receiver_balance_after,
            None,
            elapsed_seconds
        )
        conn.commit()
        return True, "Transfer successful"
        
    except Exception as e:
        # Insert error transaction record
        try:
            cursor.execute("""
                INSERT INTO transactions 
                (sender_id, receiver_id, amount, status,
                 sender_balance_before, sender_balance_after,
                 receiver_balance_before, receiver_balance_after,
                 note)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                sender_id, receiver_id, amount, "ERROR",
                sender_balance_before, sender_balance_before,
                receiver_balance_before, receiver_balance_before,
                str(e)[:200]
            ))
        except:
            pass  # Ignore error when inserting error record
        log_error(f"Transfer failed: {str(e)}")
        conn.commit()
        return False, f"Transfer failed: {str(e)}" 