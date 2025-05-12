def format_transfer_line(time, status, sender="N/A", receiver="N/A", amount="0.00",
                        sender_before="0.00", sender_after="0.00",
                        receiver_before="0.00", receiver_after="0.00", note=""):
    """
    Format a transfer status line with consistent layout
    
    Args:
        time: Current time in seconds
        status: Transaction status
        sender: Sender account name
        receiver: Receiver account name
        amount: Transfer amount
        sender_before: Sender balance before transfer
        sender_after: Sender balance after transfer
        receiver_before: Receiver balance before transfer
        receiver_after: Receiver balance after transfer
        note: Additional note or error message
        
    Returns:
        str: Formatted status line with error handling
    """
    try:
        # Type conversion and validation
        time = int(time)
        status = str(status)[:11]  # Limit status length
        
        # Handle numeric types
        try:
            amount = float(amount)
            sender_before = float(sender_before)
            sender_after = float(sender_after)
            receiver_before = float(receiver_before)
            receiver_after = float(receiver_after)
        except (ValueError, TypeError):
            # Use default values if number conversion fails
            amount = 0.00
            sender_before = 0.00
            sender_after = 0.00
            receiver_before = 0.00
            receiver_after = 0.00
        
        # Handle string types
        sender = str(sender)[:8]  # Limit length
        receiver = str(receiver)[:8]
        note = str(note)
        
        # Format output
        return (f"{time:>3}s   {status:<11} {sender:<8} {receiver:<8} "
                f"{amount:>8.2f} USD    "
                f"{sender_before:>8.2f}->{sender_after:<8.2f}    "
                f"{receiver_before:>8.2f}->{receiver_after:<8.2f}    "
                f"{note}")
                
    except Exception as e:
        # Return error message line when any error occurs
        error_msg = f"Format error: {str(e)}"
        return (f"{0:>3}s   {'ERROR':<11} {'N/A':<8} {'N/A':<8} "
                f"{0.00:>8.2f} USD    "
                f"{0.00:>8.2f}->{0.00:<8.2f}    "
                f"{0.00:>8.2f}->{0.00:<8.2f}    "
                f"{error_msg}")

def print_transfer_header():
    """Print the transfer status table header"""
    try:
        print("\nStarting transfer transactions...")
        print("-" * 160)
        print("Time   Status      Sender   Receiver   Amount         Sender Balance        Receiver Balance     Note")
        print("-" * 160)
    except Exception as e:
        print("\nError printing header:", str(e))
        # Print simplified header
        print("\nTransfer Status:")
        print("-" * 50) 