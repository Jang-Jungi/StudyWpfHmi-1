import RPi.GPIO as GPIO
import time

redPin = 18
greenPin = 23
bluePin = 24

GPIO.setmode(GPIO.BCM) # BOARD or BCM
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)
GPIO.setup(bluePin, GPIO.OUT)
print('RGB LED Test!')

if __name__ == '__main__':
    try:
        while True:
            GPIO.output(bluePin, False)
            GPIO.output(redPin, True)
            time.sleep(5)
            GPIO.output(redPin, False)
            GPIO.output(greenPin, True)
            time.sleep(5)
            GPIO.output(greenPin, False)
            GPIO.output(bluePin, True)
            time.sleep(5)
    except KeyboardInterrupt:
        print("Test terminated!")
        GPIO.output(redPin, False)
        GPIO.output(greenPin, False)
        GPIO.output(bluePin, False)
