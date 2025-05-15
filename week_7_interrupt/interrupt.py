#!/usr/bin/env python3

# Import the RPi.GPIO library to control the GPIO pins
import RPi.GPIO as GPIO
# Import the time library to allow the main loop to sleep
import time

# --- Configuration ---

# Define the GPIO pin number that the LED is connected to.
# We are using the BCM (Broadcom) numbering scheme, where 18 refers to GPIO18.
# On the physical header, this is pin 12.
LED_PIN = 18

# Define the GPIO pin number that the Button is connected to.
# We are using the BCM numbering scheme, where 23 refers to GPIO23.
# On the physical header, this is pin 16.
BUTTON_PIN = 23

# Define a variable to help with debouncing the button press.
# Buttons aren't perfect switches; they can 'bounce' when pressed or released,
# causing multiple rapid high/low transitions.
# bouncetime is specified in milliseconds (ms). 300ms is a reasonable value.
BUTTON_BOUNCETIME = 300 # milliseconds

# --- Callback Function (Interrupt Service Routine equivalent in user space) ---

# This function will be called by the RPi.GPIO library when the event
# (button press) is detected on the specified pin.
# It takes one argument, 'channel', which is the pin number that triggered the event.
def button_callback(channel):
    """
    Callback function executed when the button is pressed (falling edge detected).
    Toggles the state of the LED.
    """
    print(f"--- Button pressed on channel {channel}! ---") # Verbose print statement

    # Read the current state of the LED pin.
    current_led_state = GPIO.input(LED_PIN)

    # Determine the new state for the LED.
    # If the LED is currently HIGH (ON), set it to LOW (OFF).
    # If the LED is currently LOW (OFF), set it to HIGH (ON).
    new_led_state = GPIO.LOW if current_led_state == GPIO.HIGH else GPIO.HIGH

    # Set the LED pin to the new state.
    GPIO.output(LED_PIN, new_led_state)

    # Add a print statement to confirm the LED state change.
    print(f"LED state toggled to { 'ON' if new_led_state == GPIO.HIGH else 'OFF' }.")


# --- Main Program Execution ---

def main():
    """
    Main function to set up GPIO, register interrupt event, and run the main loop.
    """
    print("Setting up GPIO for button and LED...")

    # Set the GPIO mode.
    # GPIO.BCM: Refers to the Broadcom SOC channel names (GPIO numbers). This is the recommended mode.
    # GPIO.BOARD: Refers to the physical pin numbers on the header (less recommended as it can change between Pi models).
    GPIO.setmode(GPIO.BCM)

    # --- Configure GPIO Pins ---

    # Set up the LED pin as an output.
    # We can specify an initial value (optional), here we ensure it's OFF initially.
    GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)
    print(f"GPIO {LED_PIN} (LED) configured as output, initially LOW.")

    # Set up the Button pin as an input.
    # We configure an internal pull-up resistor because the button is connected to GND.
    # This ensures the pin is HIGH when the button is not pressed.
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    print(f"GPIO {BUTTON_PIN} (Button) configured as input with internal pull-up.")

    # --- Register the Event Detection ---

    # This is the core of the "interrupt-based" approach in user space.
    # We tell the library to call our 'button_callback' function
    # whenever a falling edge is detected on the BUTTON_PIN.
    # GPIO.FALLING: Detects transition from HIGH to LOW (happens when button is pressed in our setup).
    # GPIO.RISING: Detects transition from LOW to HIGH.
    # GPIO.BOTH: Detects any change (rising or falling edge).
    # callback=button_callback: Specifies the function to call when the event occurs.
    # bouncetime=BUTTON_BOUNCETIME: Ignores further transitions for this duration after the first one,
    #                                helping to prevent multiple triggers from a single button press.
    GPIO.add_event_detect(
        BUTTON_PIN,
        GPIO.FALLING,
        callback=button_callback,
        bouncetime=BUTTON_BOUNCETIME
    )
    print(f"Event detection added on GPIO {BUTTON_PIN} for FALLING edge with bouncetime={BUTTON_BOUNCETIME}ms.")
    print("Ready! Press the button to toggle the LED. Press Ctrl+C to exit.")

    # --- Main Program Loop ---

    # The main loop simply keeps the script running.
    # The actual work of responding to the button press is handled asynchronously
    # by the RPi.GPIO library calling the 'button_callback' function.
    # We use a try/except block to catch a KeyboardInterrupt (Ctrl+C) to allow graceful exit.
    try:
        # In a real application, this loop could be performing other tasks.
        # For this example, we just make it sleep to prevent it from
        # consuming excessive CPU while waiting for button presses.
        while True:
            # Sleep for a short duration. This loop is not doing any polling itself.
            time.sleep(1)
            # print("Main loop is running (doing other stuff or sleeping)...") # Optional: uncomment to see the main loop is still active

    except KeyboardInterrupt:
        # This block is executed if the user presses Ctrl+C.
        print("\nCtrl+C detected. Exiting gracefully.")

    finally:
        # This block is executed when the try or except block finishes.
        # It's crucial to clean up the GPIO settings to release the pins.
        # This prevents issues with future scripts using the same pins.
        GPIO.cleanup()
        print("GPIO cleaned up. Goodbye!")

# Check if the script is being run directly
if __name__ == "__main__":
    # Call the main function to start the program
    main()