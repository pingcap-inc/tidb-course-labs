import os
import sys
from datetime import datetime, timedelta
import time
import asyncio
# import queue
import multiprocessing
import signal
import atexit

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

import random
from decimal import Decimal

from database.db_connection import get_cursor, DatabaseConnectionError
from app.transfer import transfer_amount
from app.logger import setup_logger, log_error
from utils.format_utils import format_transfer_line, print_transfer_header
# from utils.queue_utils import db_result_queue

stop_event = multiprocessing.Event()
transfer_stats = {'successful': 0, 'failed': 0}
# stats_lock = multiprocessing.Lock()
connection_retry_delay = 5  # seconds
connection_status = {'is_connected': True}
# connection_lock = multiprocessing.Lock()

def signal_handler(signum, frame):
    stop_event.set()
    print("\n\nProgram terminating, please wait...")
    time.sleep(2)
    print_summary(time.time() - start_time)
    sys.exit(0)

def cleanup():
    stop_event.set()
    time.sleep(1)

def print_summary(total_time):
    """Print transfer summary"""
    print("\nTransfer Summary:")
    print(f"Successful transfers: {transfer_stats['successful']}")
    print(f"Failed transfers: {transfer_stats['failed']}")
    print(f"Total time: {total_time:.2f} seconds")

# Register signal handler
signal.signal(signal.SIGINT, signal_handler)
atexit.register(cleanup)

def get_accounts(cursor):
    """Get available accounts from database"""
    cursor.execute("""
        SELECT account_id, account_name, balance 
        FROM banking_system.accounts
    """)
    accounts = cursor.fetchall()
    
    if len(accounts) < 2:
        raise ValueError("Insufficient accounts to perform transfers")
    return accounts

def get_latest_transaction(cursor):
    """Get the latest transaction record"""
    try:
        cursor.execute("""
            SELECT 
                t.transaction_id,
                t.status,
                t.amount,
                t.created_at,
                s.account_name as sender_name,
                r.account_name as receiver_name,
                t.sender_balance_before,
                t.sender_balance_after,
                t.receiver_balance_before,
                t.receiver_balance_after,
                t.note
            FROM banking_system.transactions t
            JOIN banking_system.accounts s ON t.sender_id = s.account_id
            JOIN banking_system.accounts r ON t.receiver_id = r.account_id
            ORDER BY t.created_at DESC
            LIMIT 1
        """)
        return cursor.fetchone()
    except Exception as e:
        print(f"Error in get latest transaction: {str(e)}")

def execute_transfers(host, db_result_queue):
    """multiprocessing function to execute transfers"""
    try:
        while not stop_event.is_set():
            time.sleep(1)
            try:
                with get_cursor(host) as (cursor, conn):
                    try:
                        # Get 2 transfer accounts
                        try:
                            accounts = get_accounts(cursor)
                        except ValueError as e:
                            db_result_queue.put(('BUSI_ERROR', str(e)))
                            log_error(f"Insufficient accounts to perform transfers")                            
                            continue
                        # Execute transfer transaction
                        sender, receiver = random.sample(accounts, 2)
                        amount = Decimal(str(random.randrange(1, 11) * 100)).quantize(Decimal('0.00'))
                        
                        success, message = transfer_amount(
                            sender['account_id'],
                            receiver['account_id'],
                            amount,
                            cursor,
                            conn
                        )
                        # Update statistics
                        if success:
                            transfer_stats['successful'] += 1
                            # Get & send the last transaction record
                            try:
                                data = {
                                    'status': 'SUCCESS',
                                    'sender_name': sender['account_name'],
                                    'receiver_name': receiver['account_name'],
                                    'amount': amount,
                                    'sender_balance_before': sender['balance'],
                                    'sender_balance_after': sender['balance'] - amount,
                                    'receiver_balance_before': receiver['balance'],
                                    'receiver_balance_after': receiver['balance'] + amount,
                                    'note': ''
                                }
                                db_result_queue.put(('SUCCESS', data))
                                continue
                            except Exception as e:
                                db_result_queue.put(('DB_ERROR', f"Database error: {str(e)}"))
                                continue
                        else:
                            # Business error, such as insuficient balance
                            db_result_queue.put(('BUSI_ERROR', message))
                            transfer_stats['failed'] += 1
                            continue
                            
                    except Exception as e:
                        # Business exception
                        transfer_stats['failed'] += 1
                        db_result_queue.put(('BUSI_ERROR', f"Transaction failed: {str(e)}"))
                        continue
            except DatabaseConnectionError as e:
                # Handle database exception
                log_error(f"Database connection lost: {e}")
                # Send database error message to queue
                db_result_queue.put(('DB_ERROR', f"Database error: {str(e)}"))
                # time.sleep(connection_retry_delay)
                continue
            except Exception as e:
                # 处理其他异常
                log_error(f"Error in transfer: {str(e)}")
                db_result_queue.put(('DB_ERROR', f"System error: {str(e)}"))
                continue

    except Exception as e:
        print(f"Error in transfer multiprocessing: {str(e)}")
        stop_event.set()

def print_transfer_status(db_result_queue):
    """multiprocessing function to print transfer status"""
    current_second = 0
    
    while not stop_event.is_set():
        time.sleep(1)

        # Check if current_second is a multiple of 30
        if current_second % 30 == 0:
            print_transfer_header()  # Print header every 30 seconds
        current_second += 1

        try:
            try:
                try:
                    status, data = db_result_queue.get_nowait()
                except multiprocessing.Queue.empty:
                    line = format_transfer_line(current_second, 'WAIT', note='Waiting for transaction...')
                    print(line)
                    continue
                # Successful transfer transaction
                if status == 'SUCCESS' and data :
                    line = format_transfer_line(
                        current_second,
                        data['status'],
                        data['sender_name'],
                        data['receiver_name'],
                        data['amount'],
                        data['sender_balance_before'],
                        data['sender_balance_after'],
                        data['receiver_balance_before'],
                        data['receiver_balance_after'],
                        data['note'] or ''
                    )
                    print(line)
                
                # Business error
                elif status == 'BUSI_ERROR':
                    # Check if data contains full transaction info
                    if isinstance(data, dict) and data.get('amount', 0) > 0:
                        line = format_transfer_line(
                            current_second,
                            data['status'],
                            data['sender_name'],
                            data['receiver_name'],
                            data['amount'],
                            data['sender_balance_before'],
                            data['sender_balance_after'],
                            data['receiver_balance_before'],
                            data['receiver_balance_after'],
                            data['note']
                        )
                    else:
                        # Basic error info
                        line = format_transfer_line(
                            current_second,
                            status,
                            note=str(data)
                        )
                    print(line)
                
                # Database error
                elif status == 'DB_ERROR':
                    # Check if data contains full transaction info
                    if isinstance(data, dict) and data.get('amount', 0) > 0:
                        line = format_transfer_line(
                            current_second,
                            data['status'],
                            data['sender_name'],
                            data['receiver_name'],
                            data['amount'],
                            data['sender_balance_before'],
                            data['sender_balance_after'],
                            data['receiver_balance_before'],
                            data['receiver_balance_after'],
                            data['note']
                        )
                    else:
                        # Basic error info
                        line = format_transfer_line(
                            current_second,
                            status,
                            note=str(data)
                        )
                    print(line)
                # Database retry
                elif status == 'DB_RETRY':
                    line = format_transfer_line(current_second, status, note=str(data))
                    print(line)
                # Database recovery
                elif status == 'DB_RECOVERED':
                    line = format_transfer_line(current_second, status, note=str(data))
                    print(line)
                else:
                    line = format_transfer_line(current_second, status, note=str(data))
                    print(line)
            except Exception as e:
                line = format_transfer_line(current_second, 'WAIT', note='Waiting for transaction...')
                print(line)
                continue
        except Exception as e:
            error_data = {
                'status': 'DB_ERROR',
                'sender_name': 'N/A',
                'receiver_name': 'N/A',
                'amount': 0.00,
                'sender_balance_before': 0.00,
                'sender_balance_after': 0.00,
                'receiver_balance_before': 0.00,
                'receiver_balance_after': 0.00,
                'note': str(e) 
            }
            
            line = format_transfer_line(
                current_second,
                error_data['status'],
                error_data['sender_name'],
                error_data['receiver_name'],
                error_data['amount'],
                error_data['sender_balance_before'],
                error_data['sender_balance_after'],
                error_data['receiver_balance_before'],
                error_data['receiver_balance_after'],
                error_data['note']
            )
            print(line)
            continue

def main(duration_minutes=1, host=None):
    """Main function to start transfer system"""
    global start_time
    start_time = time.time()
    setup_logger()
    db_result_queue = multiprocessing.Queue() 

    # Start transfer execution multiprocessing
    transfer_multiprocessing = multiprocessing.Process(target=execute_transfers, args=(host,db_result_queue,))
    transfer_multiprocessing.daemon = True
    transfer_multiprocessing.start()
    
    # Start status printing multiprocessing
    printer_multiprocessing = multiprocessing.Process(target=print_transfer_status, args=(db_result_queue,))
    printer_multiprocessing.daemon = True
    printer_multiprocessing.start()
    
    # Wait for specified duration
    try:
        time.sleep(duration_minutes * 60)
        stop_event.set()
        time.sleep(2)  # Wait for multiprocessings to finish
        print_summary(time.time() - start_time)
    except KeyboardInterrupt:
        stop_event.set()
        time.sleep(2)
        print_summary(time.time() - start_time)

if __name__ == "__main__":
    main(1)  # Run for 1 minute by default 