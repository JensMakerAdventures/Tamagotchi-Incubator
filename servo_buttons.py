from adafruit_servokit import ServoKit
from time import sleep

class ButtonController:
  def __init__(self, buttonL, buttonM, buttonR):
    self.buttonL = buttonL
    self.buttonM = buttonM
    self.buttonR = buttonR
    self.kit = ServoKit(channels=16)

  def __press(self, button):
    self.kit.servo[button.channel].angle = button.activateAngle
    sleep(0.5)
    self.kit.servo[button.channel].angle = button.retractAngle
    sleep(0.5)

  def pressL(self):
    self.__press(self.buttonL)
  
  def pressM(self):
    self.__press(self.buttonM)
  
  def pressR(self):
    self.__press(self.buttonR)


class TamaButton:
  def __init__(self, label, channel, retractAngle, activateAngle):
    self.label = label
    self.channel = channel
    self.retractAngle = retractAngle
    self.activateAngle = activateAngle