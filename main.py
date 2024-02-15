
import gui
import camera
import servo_buttons
import statemachine
import vision

buttonL = servo_buttons.TamaButton("left", 0, 100, 75)
buttonM = servo_buttons.TamaButton("middle", 1, 110, 75)
buttonR = servo_buttons.TamaButton("right", 2, 60, 95)

buttonController = servo_buttons.ButtonController(buttonL, buttonM, buttonR)
tamaGui = gui.TamaGui(buttonController)
tamaStatemachine = statemachine.TamaStatemachine()
tamaCam = camera.TamaCam()

buttonController.pressL()
buttonController.pressM()
buttonController.pressR()

while(True):
    image = tamaCam.preview(10)

tamaGui.mainLoop()