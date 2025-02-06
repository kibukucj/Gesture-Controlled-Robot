import serial
import time

def send_command(port, baud_rate, command):
    """
    Sends a single-character command to the Arduino via Bluetooth.
    
    Args:
        port (str): The COM port of the Bluetooth module (e.g., "COM7").
        baud_rate (int): The baud rate for serial communication (e.g., 9600).
        command (str): The command to send ('F', 'B', 'L', 'R', 'S').
    """
    try:
        # Open the Bluetooth serial connection
        with serial.Serial(port, baud_rate, timeout=1) as bt:
            print(f"Sending command: {command}")
            bt.write(command.encode('utf-8'))  # Send the command
            time.sleep(0.5)  # Short delay to ensure command is processed
            
            # Optionally read and print feedback from the Arduino (if any)
            if bt.in_waiting > 0:
                feedback = bt.readline().decode('utf-8').strip()
                print(f"Arduino Response: {feedback}")
    except serial.SerialException as e:
        print(f"Serial exception: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    port = "COM7"  # Replace with your HC-05's COM port
    baud_rate = 9600
    
    print("Robot Control via Python")
    print("Commands: F (Forward), B (Backward), L (Left), R (Right), S (Stop), Q (Quit)")
    
    while True:
        command = input("Enter command: ").strip().upper()
        if command in ['F', 'B', 'L', 'R', 'S']:
            send_command(port, baud_rate, command)
        elif command == 'Q':  # Quit the script
            print("Exiting...")
            break
        else:
            print("Invalid command. Try again.")