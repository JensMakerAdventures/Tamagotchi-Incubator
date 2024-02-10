from time import sleep
import tkinter
import os
from picamera import PiCamera

# check if display env variable is ok
if os.environ.get('DISPLAY','') == '':
    #print('No $DISPLAY env variable, so using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

master = tkinter.Tk()
master.attributes('-fullscreen',True)
master.title("Tamagotchi-Incubator")

camera = PiCamera()
#camera.resolution = (800, 600)
camera.framerate = 15
camera.start_preview()
sleep(5)
camera.capture('test.jpg')
camera.stop_preview()

master.mainloop()
