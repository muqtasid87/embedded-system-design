# Import necessary libraries
from gpiozero import Servo
from time import sleep

# --- Configuration ---
# GPIO Pin number (BCM numbering)
SERVO_PIN = 17  # Example GPIO pin for the servo

# --- Initialize Device ---
try:
    # Servo Motor
    # The Servo class uses software PWM.
    # min_pulse_width and max_pulse_width might need adjustment for your specific servo.
    # Default is 1ms (min) to 2ms (max) for a 50Hz frequency (20ms period).
    # Common values for many servos are 0.5ms to 2.5ms pulse widths.
    servo = Servo(SERVO_PIN, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)
    print(f"Servo motor initialized on GPIO {SERVO_PIN}")

except Exception as e:
    print(f"Error initializing servo: {e}")
    print("Make sure you have gpiozero installed (sudo pip3 install gpiozero)")
    print("And that you are running this script on a Raspberry Pi, possibly with sudo privileges.")
    exit()

# --- Main Control Logic ---
def run_servo():
    print("\n--- Starting Servo Motor Demonstration ---")

    # Move Servo
    print("Moving Servo to minimum position...")
    servo.min()
    sleep(1) # Wait for the servo to reach the position

    print("Moving Servo to middle position...")
    servo.mid()
    sleep(1)

    print("Moving Servo to maximum position...")
    servo.max()
    sleep(1)

    print("Returning Servo to middle position...")
    servo.mid()
    sleep(1)

    print("Servo movement complete.")
    print("\n--- Servo Motor Demonstration Finished ---")

if __name__ == "__main__":
    try:
        run_servo()
    except KeyboardInterrupt:
        print("\nExiting program. Detaching servo.")
    finally:
        # Ensure the servo is properly detached and resources are released
        if 'servo' in locals() and servo:
            print("Detaching servo (setting value to None)...")
            servo.value = None  # Detach the servo, stopping PWM signals
            servo.close()       # Release GPIO resources
            print("Servo detached and resources closed.")
