import requests
import time

# ESP32 IP address
esp32_ip = "192.168.137.37"  # Replace with your ESP32's IP address

# LED control functions
def turn_led_on():
    try:
        response = requests.get(f"http://{esp32_ip}/led/on")
        if response.status_code == 200:
            print("LED turned ON")
    except Exception as e:
        print(f"Error turning LED on: {e}")

def turn_led_off():
    try:
        response = requests.get(f"http://{esp32_ip}/led/off")
        if response.status_code == 200:
            print("LED turned OFF")
    except Exception as e:
        print(f"Error turning LED off: {e}")

# Blink the LED based on input
def blink_led(times, delay):
    for _ in range(times):
        turn_led_on()
        time.sleep(delay)
        turn_led_off()
        time.sleep(delay)

# Example usage: Blink LED 5 times with a delay of 1 second
if __name__ == "__main__":
    blink_led(times=5, delay=1)
