
import gui
import camera
import servo_buttons
import statemachine
import vision
import os
from time import sleep

# This line is essential, do not remove. This makes sure you can display to the 3.5 inch display
os.environ.__setitem__('DISPLAY', ':0.0') 

buttonL = servo_buttons.TamaButton("left", 0, 140, 75)
buttonM = servo_buttons.TamaButton("middle", 1, 150, 75)
buttonR = servo_buttons.TamaButton("right", 2, 20, 95)

buttonController = servo_buttons.ButtonController(buttonL, buttonM, buttonR)
tamaGui = gui.TamaGui(buttonController)
tamaStatemachine = statemachine.TamaStatemachine()
tamaCam = camera.TamaCam()
tamaVision = vision.TamaVision()

#buttonController.pressL()
#buttonController.pressM()
#buttonController.pressR()

#while(True):
#tamaCam.calibrate()
testString = 'frame.jpg'
frame = tamaCam.getFrameToFile(testString)
tamaVision.findPattern(testString, 'angel.png')
#while(True):
    #tamaGui.mainLoop()
    #tamaVision.findPattern('frame.jpg', 'angel.png')