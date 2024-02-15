
import gui
import camera
import servo_buttons
import statemachine
import vision

import os

buttonL = servo_buttons.TamaButton("left", 0, 100, 75)
buttonM = servo_buttons.TamaButton("middle", 1, 110, 75)
buttonR = servo_buttons.TamaButton("right", 2, 60, 95)

buttonController = servo_buttons.ButtonController(buttonL, buttonM, buttonR)
tamaGui = gui.TamaGui()
tamaStatemachine = statemachine.TamaStatemachine()


buttonController.pressL()
buttonController.pressM()
buttonController.pressR()

image = camera.getFrame()
pattern = vision.getPattern('poop')
vision.findPattern(image, 'poop')

tamaGui.mainLoop()