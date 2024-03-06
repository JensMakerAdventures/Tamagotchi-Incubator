import gui
import camera
import servo_buttons
import controller
import vision
import log
import os
import light
from time import sleep

# This line is essential, do not remove. This makes sure you can display to the 3.5 inch display
os.environ.__setitem__('DISPLAY', ':0.0') 

buttonL = servo_buttons.TamaButton("left", 0, 170, 75)
buttonM = servo_buttons.TamaButton("middle", 1, 170, 75)
buttonR = servo_buttons.TamaButton("right", 2, 0, 90)

tamaButtons = servo_buttons.ButtonController(buttonL, buttonM, buttonR)
tamaGui = gui.TamaGui(tamaButtons)
tamaCam = camera.TamaCam()
tamaVision = vision.TamaVision()
tamaLog = log.TamaLog()
tamaLight = light.TamaLight(14)
tamaController = controller.TamaController(tamaCam, tamaVision, tamaButtons, tamaLog, tamaLight)


#buttonController.pressL()
#buttonController.pressM()
#buttonController.pressR()
#tamaCam.calibrate()
#tamaGui.mainLoop()
#testString = 'frame.jpg'
#frame = tamaCam.getFrameToFile(testString)
#tamaVision.findPattern(testString, 'angel.png')

while(True):
    #tamaLight.strobe(False, 5, 0.4)
    #tamaButtons.pressL()
    if True:                     
        tamaCam.preview()          
        tamaController.getAndHandleState()
    else:
        tamaGui.mainLoop()