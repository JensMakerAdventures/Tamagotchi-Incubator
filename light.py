import RPi.GPIO as GPIO
from time import sleep

class TamaLight(object):
    def __init__(self, lightPin):
        GPIO.setmode(GPIO.BCM)
        self.lightPin = lightPin
        GPIO.setup(self.lightPin, GPIO.OUT)
        self.turnOff()

    def strobe(self, endState, nStrobes, interval):
        for x in range(nStrobes):
            self.turnOn()
            sleep(interval)
            self.turnOff()
            sleep(interval)
        if (endState == True):
            self.turnOn()

    def turnOn(self):
        GPIO.output(self.lightPin, GPIO.HIGH)

    def turnOff(self):
        GPIO.output(self.lightPin, GPIO.LOW)