from time import sleep
import tkinter
import os
from picamera import PiCamera
from adafruit_servokit import ServoKit

class Button:
  def __init__(self, label, channel, retractAngle, activateAngle):
    self.label = label
    self.channel = channel
    self.retractAngle = retractAngle
    self.activateAngle = activateAngle

  def press(self):
    kit.servo[self.channel].angle = self.activateAngle
    sleep(0.5)
    kit.servo[self.channel].angle = self.retractAngle
    sleep(0.5)

buttonL = Button("left", 0, 100, 75)
buttonM = Button("middle", 1, 110, 75)
buttonR = Button("right", 2, 60, 95)

# Servo's
kit = ServoKit(channels=16)










'''
# check if display env variable is ok
if os.environ.get('DISPLAY','') == '':
    #print('No $DISPLAY env variable, so using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

master = tkinter.Tk()
master.attributes('-fullscreen',True)
master.title("Tamagotchi-Incubator")
'''

while(True):
  buttonL.press()
  buttonM.press()
  buttonR.press()


'''
camera = PiCamera()
#camera.resolution = (800, 600)
camera.framerate = 15
camera.start_preview()
sleep(5)
camera.capture('test.jpg')
camera.stop_preview()

master.mainloop()
'''