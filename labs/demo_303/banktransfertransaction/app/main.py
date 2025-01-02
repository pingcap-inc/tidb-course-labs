import os
import sys
from datetime import datetime, timedelta
import time
import threading
import signal
import atexit
from queue import Queue, Empty

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

import random
from decimal import Decimal

from database.db_connection import get_cursor, DatabaseConnectionError
from app.transfer import transfer_amount
from app.logger import setup_logger, log_error
from utils.format_utils import format_transfer_line, print_transfer_header
from utils.queue_utils import db_result_queue

stop_event = threading.Event()
transfer_stats = {'successful': 0, 'failed': 0}
stats_lock = threading.Lock()
connection_retry_delay = 5  # seconds
connection_status = {'is_connected': True}
connection_lock = threading.Lock()

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

def execute_transfers():
    """Thread function to execute transfers"""
    try:
        while not stop_event.is_set():
            try:
                with get_cursor() as (cursor, conn):
                    with connection_lock:
                        connection_status['is_connected'] = True
                    
                    try:
                        # 获取账户信息
                        try:
                            accounts = get_accounts(cursor)
                        except ValueError as e:
                            db_result_queue.put(('BUSI_ERROR', str(e)))
                            log_error(f"Insufficient accounts to perform transfers")
                            time.sleep(1)
                            continue
                        
                        # 执行转账交易
                        sender, receiver = random.sample(accounts, 2)
                        amount = Decimal(str(random.randrange(1, 11) * 100)).quantize(Decimal('0.00'))
                        
                        success, message = transfer_amount(
                            sender['account_id'],
                            receiver['account_id'],
                            amount,
                            cursor,
                            conn
                        )
                        
                        # 更新统计信息
                        with stats_lock:
                            if success:
                                transfer_stats['successful'] += 1
                            else:
                                # 业务错误（如余额不足）
                                db_result_queue.put(('BUSI_ERROR', message))
                                transfer_stats['failed'] += 1
                                time.sleep(1)
                                continue
                            
                        # 获取并发送最新交易记录
                        latest_transaction = get_latest_transaction(cursor)
                        db_result_queue.put(('SUCCESS', latest_transaction))
                        
                    except Exception as e:
                        # 处理业务异常
                        with stats_lock:
                            transfer_stats['failed'] += 1
                        db_result_queue.put(('BUSI_ERROR', f"Transaction failed: {str(e)}"))
                        
                    time.sleep(1)  # Execute one transfer per second
                    
            except DatabaseConnectionError as e:
                # 处理数据库连接异常
                with connection_lock:
                    connection_status['is_connected'] = False
                log_error(f"Database connection lost: {e}")
                db_result_queue.put(('DB_ERROR', f"Database error: {str(e)}"))
                time.sleep(connection_retry_delay)
            except Exception as e:
                # 处理其他异常
                log_error(f"Error in transfer: {str(e)}")
                db_result_queue.put(('DB_ERROR', f"System error: {str(e)}"))
                time.sleep(1)

    except Exception as e:
        print(f"Error in transfer thread: {str(e)}")
        stop_event.set()

def print_transfer_status():
    """Thread function to print transfer status"""
    current_second = 0
    last_transaction_id = None
    
    # Print header
    print_transfer_header()
    
    while not stop_event.is_set():
        current_second += 1
        
        try:
            try:
                status, data = db_result_queue.get(timeout=0.1)
                
                # Successful transfer transaction
                if status == 'SUCCESS' and data and data['transaction_id'] != last_transaction_id:
                    last_transaction_id = data['transaction_id']
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
                    line = format_transfer_line(current_second, status, note=str(data))
                    print(line)
                
                # Database error
                elif status == 'DB_ERROR':
                    line = format_transfer_line(current_second, status, note=str(data))
                    print(line)
                
                # Database retry
                elif status == 'DB_RETRY':
                    line = format_transfer_line(current_second, status, note=str(data))
                    print(line)
                
                # Database recovery
                elif status == 'DB_RECOVERED':
                    line = format_transfer_line(current_second, status, note=str(data))
                    print(line)
                
            except Empty:
                line = format_transfer_line(current_second, 'WAIT', note='Waiting for transaction...')
                print(line)
        except Exception as e:
            with connection_lock:
                is_connected = connection_status['is_connected']
            
            status_msg = "DB ERROR" if not is_connected else "ERROR"
            print(f"{current_second:>3}s   {status_msg:<8} {'N/A':<8} {'N/A':<8} "
                  f"{'0.00':>8} USD    "
                  f"{'0.00':>8}->{0.00:<8}    "
                  f"{'0.00':>8}->{0.00:<8}    "
                  f"{'Connection lost...' if not is_connected else 'Processing...'}")
        
        time.sleep(1)

def main(duration_minutes=1):
    """Main function to start transfer system"""
    global start_time
    start_time = time.time()
    setup_logger()
    
    # Start transfer execution thread
    transfer_thread = threading.Thread(target=execute_transfers)
    transfer_thread.daemon = True
    transfer_thread.start()
    
    # Start status printing thread
    printer_thread = threading.Thread(target=print_transfer_status)
    printer_thread.daemon = True
    printer_thread.start()
    
    # Wait for specified duration
    try:
        time.sleep(duration_minutes * 60)
        stop_event.set()
        time.sleep(2)  # Wait for threads to finish
        print_summary(time.time() - start_time)
    except KeyboardInterrupt:
        stop_event.set()
        time.sleep(2)
        print_summary(time.time() - start_time)

if __name__ == "__main__":
    main(1)  # Run for 1 minute by default 