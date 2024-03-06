import tkinter as tk
import os
from tkinter import messagebox

def checkSetDisplay():
    # check if display env variable is ok
    if os.environ.get('DISPLAY','') == '':
        #print('No $DISPLAY env variable, so using :0.0')
        os.environ.__setitem__('DISPLAY', ':0.0')

class TamaGui():
    def __init__(self, buttonControllerInput):
        checkSetDisplay()
        self.buttonController = buttonControllerInput
        self.gui = tk.Tk()
        #self.gui.attributes('-fullscreen',True)
        self.gui.title("Tamagotchi-Incubator")
        self.buildGUI()
        
    def buildGUI(self):
        lButton = tk.Button(self.gui, text ="Push L", command = self.buttonController.pressL)
        lButton.place(x=10,y=10)

        mButton = tk.Button(self.gui, text ="Push M", command = self.buttonController.pressM)
        mButton.place(x=10,y=40)

        rButton = tk.Button(self.gui, text ="Push R", command = self.buttonController.pressR)
        rButton.place(x=10,y=70)

        lAndRButton = tk.Button(self.gui, text ="Push L&R", command = self.buttonController.pressLandR)
        lAndRButton.place(x=10,y=100)
        
    def mainLoop(self):
        self.gui.mainloop()
