import tkinter as tk
import os
from tkinter import messagebox

def checkSetDisplay():
    # check if display env variable is ok
    if os.environ.get('DISPLAY','') == '':
        #print('No $DISPLAY env variable, so using :0.0')
        os.environ.__setitem__('DISPLAY', ':0.0')

def TamaGui():
    def __init__(self, buttonControllerInput):
        checkSetDisplay()
        buttonController = buttonControllerInput
        gui = tk.Tk()
        gui.attributes('-fullscreen',True)
        gui.title("Tamagotchi-Incubator")
        buildGUI()
        
    def buildGUI(self):
        B = tk.Button(self.gui, text ="Push L", command = self.buttonController.pressL)
        B.place(x=50,y=50)
    def mainLoop(self):
        self.gui.mainloop()