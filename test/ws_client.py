import websocket
import threading
import time
import sys

# The address of your Go Gin server's WebSocket endpoint
WEBSOCKET_URL = "ws://localhost:8080/ws"
# Flag to signal the main thread to stop
keep_running = True

def on_open(ws):
    """Called when the connection is successfully opened."""
    print("\n✅ Connection opened successfully.")
    print("Type a message and press Enter to send. Type 'exit' to quit.")
    # You can send an initial message here if needed
    # ws.send("Initial connection message.")

def on_message(ws, message):
    """Called when a message is received from the server."""
    # Print the server's response clearly
    print(f"\n⬅️ SERVER ECHO: {message}")
    # Print the prompt again so the user knows they can type
    sys.stdout.write(">> ")
    sys.stdout.flush()

def on_error(ws, error):
    """Called on connection error."""
    print(f"\n❌ WebSocket Error: {error}")
    global keep_running
    keep_running = False

def on_close(ws, close_status_code, close_msg):
    """Called when the connection is closed."""
    print(f"\n🛑 Connection closed. Code: {close_status_code}, Message: {close_msg}")
    global keep_running
    keep_running = False

def input_loop(ws):
    """
    Handles continuous input from the user in the main thread.
    """
    global keep_running
    
    # Wait briefly for the connection to open before starting the input prompt
    time.sleep(0.5) 

    while keep_running:
        try:
            # Display the prompt and wait for user input
            sys.stdout.write(">> ")
            sys.stdout.flush()
            user_input = sys.stdin.readline().strip()

            if user_input.lower() == 'exit':
                print("Closing connection...")
                ws.close()
                break

            if user_input:
                ws.send(user_input)
                # We won't print the "Client sent" message here; 
                # we'll wait for the server's echo (on_message) to confirm.
            
        except EOFError:
            # Handle Ctrl+D (end of file)
            print("Closing connection...")
            ws.close()
            break
        except Exception as e:
            # Catch other potential input errors
            print(f"Input error: {e}")
            break

# --- Main execution block ---
if __name__ == "__main__":
    print(f"Attempting to connect to: {WEBSOCKET_URL}")
    
    # Create the WebSocketApp instance
    ws = websocket.WebSocketApp(
        WEBSOCKET_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    # 1. Start the WebSocket connection in a separate thread (daemon=True means it stops 
    # when the main program finishes).
    ws_thread = threading.Thread(target=ws.run_forever, daemon=True)
    ws_thread.start()

    # 2. Run the interactive input loop in the main thread.
    input_loop(ws)

    # 3. Wait for the WebSocket thread to finish cleanup.
    ws_thread.join(timeout=1)
    print("Client script finished.")

import websocket
import threading
import time
import sys

# The address of your Go Gin server's WebSocket endpoint
WEBSOCKET_URL = "ws://localhost:8080/ws"
# Flag to signal the main thread to stop
keep_running = True

def on_open(ws):
    """Called when the connection is successfully opened."""
    print("\n✅ Connection opened successfully.")
    print("Type a message and press Enter to send. Type 'exit' to quit.")
    # You can send an initial message here if needed
    # ws.send("Initial connection message.")

def on_message(ws, message):
    """Called when a message is received from the server."""
    # Print the server's response clearly
    print(f"\n⬅️ SERVER ECHO: {message}")
    # Print the prompt again so the user knows they can type
    sys.stdout.write(">> ")
    sys.stdout.flush()

def on_error(ws, error):
    """Called on connection error."""
    print(f"\n❌ WebSocket Error: {error}")
    global keep_running
    keep_running = False

def on_close(ws, close_status_code, close_msg):
    """Called when the connection is closed."""
    print(f"\n🛑 Connection closed. Code: {close_status_code}, Message: {close_msg}")
    global keep_running
    keep_running = False

def input_loop(ws):
    """
    Handles continuous input from the user in the main thread.
    """
    global keep_running
    
    # Wait briefly for the connection to open before starting the input prompt
    time.sleep(0.5) 

    while keep_running:
        try:
            # Display the prompt and wait for user input
            sys.stdout.write(">> ")
            sys.stdout.flush()
            user_input = sys.stdin.readline().strip()

            if user_input.lower() == 'exit':
                print("Closing connection...")
                ws.close()
                break

            if user_input:
                ws.send(user_input)
                # We won't print the "Client sent" message here; 
                # we'll wait for the server's echo (on_message) to confirm.
            
        except EOFError:
            # Handle Ctrl+D (end of file)
            print("Closing connection...")
            ws.close()
            break
        except Exception as e:
            # Catch other potential input errors
            print(f"Input error: {e}")
            break

# --- Main execution block ---
if __name__ == "__main__":
    print(f"Attempting to connect to: {WEBSOCKET_URL}")
    
    # Create the WebSocketApp instance
    ws = websocket.WebSocketApp(
        WEBSOCKET_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    # 1. Start the WebSocket connection in a separate thread (daemon=True means it stops 
    # when the main program finishes).
    ws_thread = threading.Thread(target=ws.run_forever, daemon=True)
    ws_thread.start()

    # 2. Run the interactive input loop in the main thread.
    input_loop(ws)

    # 3. Wait for the WebSocket thread to finish cleanup.
    ws_thread.join(timeout=1)
    print("Client script finished.")
