import blynklib
import time

# Blynk credentials
BLYNK_TEMPLATE_ID = "TMPL3JyIHEzOC"
BLYNK_TEMPLATE_NAME = "Fan control"
BLYNK_AUTH_TOKEN = "Q2tr4nl9Aea2SLUE4s5VYXeehfEPWXwG"

# Initialize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH_TOKEN)

# Virtual pin to control
VIRTUAL_PIN = 0  # Set this to the virtual pin you want to control (V0 in this case)

# Function to check Blynk connection
def check_blynk_connection():
    if blynk.connected():  # Check if connected to the Blynk server
        print("Blynk is connected.")
        return True
    else:
        print("Blynk is not connected.")
        return False

# Function to toggle the switch state on Blynk
def toggle_blynk_switch(state):
    blynk.virtual_write(VIRTUAL_PIN, state)
    print(f"Switch is now {'ON' if state == 1 else 'OFF'}")

# Main loop
if __name__ == "__main__":
    print("Checking Blynk connection status...")
    try:
        while True:
            blynk.run()  # Handle Blynk communication

            # Check connection status
            if check_blynk_connection():
                print("Performing actions while connected...")
                
                # Example: Toggle the switch state every 5 seconds
                toggle_blynk_switch(1)  # Turn ON
                time.sleep(5)  # Wait for 5 seconds
                toggle_blynk_switch(0)  # Turn OFF
                time.sleep(5)  # Wait for 5 seconds

            else:
                print("Retrying connection...")

            # Wait before checking again
            time.sleep(5)  # Check connection status every 5 seconds

    except KeyboardInterrupt:
        print("\nExiting program.")
