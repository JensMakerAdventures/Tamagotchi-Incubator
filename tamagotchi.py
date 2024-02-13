from time import sleep
import tkinter
import os
from picamera import PiCamera
from adafruit_servokit import ServoKit

# Servo's
kit = ServoKit(channels=16)
servoLabels = ["L", "M", "R"]
servoChannels = [0, 1, 2]
servoRetractAngles = [100, 110, 60] #calibration
servoActivateAngles = [75, 75, 95] #calibration











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
  kit.servo[0].angle = 100



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