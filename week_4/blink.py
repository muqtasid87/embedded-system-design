import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
led_pin = 17
GPIO.setup(led_pin, GPIO.OUT)

try:
    while True:
        GPIO.output(led_pin, GPIO.HIGH)
        print("LED ON")  # <-- Writes to terminal
        time.sleep(1)
        GPIO.output(led_pin, GPIO.LOW)
        print("LED OFF")  # <-- Writes to terminal
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()
