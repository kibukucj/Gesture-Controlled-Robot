import speech_recognition as sr
from commandSender import send_command

def recognize_voice_commands(port="COM7", baud_rate=9600):
    """
    Listens for voice commands and sends them to the robot.
    
    Args:
        port (str): Serial port for communication with the HC-05 module.
        baud_rate (int): Baud rate for serial communication.
    """
    recognizer = sr.Recognizer()

    print("Voice Command Control Active")
    print("Say 'start', 'stop', 'left', 'right', or 'forward' to control the robot.")
    
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for commands...")
                audio = recognizer.listen(source, timeout=5)
                
                # Recognize the voice command
                command = recognizer.recognize_google(audio).lower()
                print(f"Voice Command Detected: {command}") 
                
                # Map voice commands to robot commands
                if command in ['start', 'forward']:
                    send_command(port, baud_rate, 'forward')
                elif command == 'stop':
                    send_command(port, baud_rate, 'stop')
                elif command == 'left':
                    send_command(port, baud_rate, 'left')
                elif command == 'right':
                    send_command(port, baud_rate, 'right')
                elif command == 'backward':
                    send_command(port, baud_rate, 'backward')
                elif command == 'quit':  # Special command to exit
                    print("Exiting voice control.")
                    break
                else:
                    print("Unknown command. Please try again.")
        
        except sr.UnknownValueError:
            print("Could not understand the audio. Please speak clearly.")
        except sr.RequestError as e:
            print(f"Error with the speech recognition service: {e}")
        except sr.WaitTimeoutError:
            print("Listening timeout. Please try again.")
        except KeyboardInterrupt:
            print("Voice control interrupted.")
            break

if __name__ == "__main__":
    # Specify the port and baud rate here or use defaults
    recognize_voice_commands(port="COM7", baud_rate=9600)
