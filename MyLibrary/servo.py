import pigpio
from time import sleep

class Servo:
    def __init__(self, pin: int) -> None:
        print("Initialize Servo")
        self.pi = pigpio.pi()
        self.servoPin = pin
        self.pi.set_servo_pulsewidth(self.servoPin, 0)
        self.close()

    def open(self):
        print("Pintu Terbuka")
        self.pi.set_servo_pulsewidth(self.servoPin, 1500)
        sleep(1)

    def close(self):
        print("Pintu Tertutup")
        self.pi.set_servo_pulsewidth(self.servoPin, 500)
        sleep(1)

    def stop(self):
        print("Stop Servo")
        self.pi.set_servo_pulsewidth(self.servoPin, 0)
        self.pi.stop()

if __name__ == "__main__":
    # servo = Servo(pin=13)
    servo = Servo()
    servo.open()
    servo.close()
    servo.stop()

