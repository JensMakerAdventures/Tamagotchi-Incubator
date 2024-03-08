import gui
import camera
import servo_buttons
import controller
import vision
from datetime import datetime
import logging
import os
import light
from time import sleep
import threading


# This line is essential, do not remove. This makes sure you can display to the 3.5 inch display
os.environ.__setitem__('DISPLAY', ':0.0') 

buttonL = servo_buttons.TamaButton("left", 0, 170, 75)
buttonM = servo_buttons.TamaButton("middle", 1, 170, 75)
buttonR = servo_buttons.TamaButton("right", 2, 0, 90)

tamaButtons = servo_buttons.ButtonController(buttonL, buttonM, buttonR)
tamaGui = gui.TamaGui(tamaButtons)
tamaCam = camera.TamaCam()
# Threshold offset: higher means more black pixels. Normally +0.02 is ok
# positiveThreshold: 0.40 is good, little valse positives. value above this means we've found the pattern
tamaVision = vision.TamaVision(0.40, 0.02, False)
tamaLight = light.TamaLight(14)
tamaController = controller.TamaController(tamaCam, tamaVision, tamaButtons, tamaLight)

now = datetime.now()
date_time = now.strftime("%Y-%m-%d %H:%M")
logging.basicConfig(filename=('logs/' + str(date_time) + '.log'), level=logging.INFO, format='%(message)s')

#logger = logging.getLogger('Tamagotchi logger')

logging.log(logging.CRITICAL, 'Test Jens')
def threadedMainLogic():
    while True:
        if tamaGui.autoMode:
            tamaController.getAndHandleState(tamaGui.loveMode)

tamaCam.preview()  
while(True):
    t = threading.Thread(target=threadedMainLogic)
    t.start()
    tamaGui.mainloop()
    
    
