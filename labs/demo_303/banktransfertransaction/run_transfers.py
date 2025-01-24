import sys
import time
import argparse
import os
from datetime import datetime, timedelta

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from app.main import main as execute_main

def run_timed_transfers(duration_minutes):
    """
    Execute timed transfer transactions
    Execute one transfer per second for the specified duration in minutes
    """
    # Calculate total number of transfers
    transfers_per_second = 1
    total_seconds = duration_minutes * 60
    total_transfers = total_seconds * transfers_per_second
    
    # Print start information
    print(f"\nStarting timed transfers...")
    print(f"Duration: {duration_minutes} minutes")
    print(f"Frequency: {transfers_per_second} transfers/second")
    print(f"Total planned transfers: {total_transfers}")
    print("\n" + "=" * 50 + "\n")
    
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=duration_minutes)
    
    current_second = start_time.second
    transfers_this_second = 0
    total_executed = 0
    
    while datetime.now() < end_time:
        now = datetime.now()
        
        # Reset counter when entering a new second
        if now.second != current_second:
            current_second = now.second
            transfers_this_second = 0
        
        # Execute transfer if not reached the limit for current second
        if transfers_this_second < transfers_per_second:
            execute_random_transfers(1)
            transfers_this_second += 1
            total_executed += 1
            
            # Brief wait if not reached the per-second limit
            if transfers_this_second < transfers_per_second:
                time.sleep(0.2)
        else:
            # Wait for next second if reached the limit
            time.sleep(0.1)
    
    # Print completion statistics
    print("\n" + "=" * 50)
    print("\nTransfer execution completed!")
    print(f"Planned transfers: {total_transfers}")
    print(f"Actual transfers: {total_executed}")
    print(f"Total time: {(datetime.now() - start_time).total_seconds():.2f} seconds")

def main():
    parser = argparse.ArgumentParser(description='Execute timed transfer transactions')
    parser.add_argument('duration', type=int, help='Execution duration (minutes)')
    parser.add_argument('--host', type=str, default='127.0.0.1',
                       help='TiDB server host address (default: 127.0.0.1)')
    args = parser.parse_args()
    
    if args.duration <= 0:
        print("Execution duration must be greater than 0 minutes")
        sys.exit(1)
    
    # Set TiDB host in environment variable
    os.environ['TIDB_HOST'] = args.host
    
    try:
        print(f"\nConnecting to TiDB server at {args.host}...")
        execute_main(args.duration)
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"\nExecution error: {str(e)}")

if __name__ == "__main__":
    main() 