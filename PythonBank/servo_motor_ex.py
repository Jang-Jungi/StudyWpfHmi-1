import RPi.GPIO as GPIO
import time

servoPin = 17   # 서보핀
SERVO_MAX = 12  # 서보모터의 최대(180도) 위치 주기
SERVO_MIN = 3   # 서보모터의 최소(0도) 위치 주기

GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPin, GPIO.OUT)

servo = GPIO.PWM(servoPin, 50)
servo.start(0)
print('SERVO MOTOR Test!')

def setServoPos(degree):
    if degree > 180:
        degree = 180

    # degree를 duty로 변경
    duty = SERVO_MIN + (degree*(SERVO_MAX-SERVO_MIN)/180.0)
    # duty value 출력
    print('Degree: {} to {}(Duty)'.format(degree, duty))

    # 변경된 duty value를 서보 PWM 적용
    servo.ChangeDutyCycle(duty)


if __name__ == '__main__':
    try:
        while True:
            setServoPos(0)
            time.sleep(1)
            setServoPos(90)
            time.sleep(1)
            setServoPos(120)
            time.sleep(1)
            setServoPos(180)
            time.sleep(1)
    except KeyboardInterrupt:
        servo.stop()
        GPIO.cleanup()
        print("Test terminated!")
