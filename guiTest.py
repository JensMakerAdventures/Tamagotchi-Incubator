import gui
import servo_buttons
import camera
import os

buttonL = servo_buttons.TamaButton("left", 0, 170, 75)
buttonM = servo_buttons.TamaButton("middle", 1, 170, 75)
buttonR = servo_buttons.TamaButton("right", 2, 0, 90)

# This line is essential, do not remove. This makes sure you can display to the 3.5 inch display
os.environ.__setitem__('DISPLAY', ':0.0') 

tamaButtons = servo_buttons.ButtonController(buttonL, buttonM, buttonR)
tamaGui = gui.TamaGui(tamaButtons)
tamaCam = camera.TamaCam()

while True:
    tamaCam.preview()  
    tamaGui.mainLoop()