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
        B = tk.Button(self.gui, text ="Push L", command = self.buttonController.pressL)
        B.place(x=50,y=50)
        
    def mainLoop(self):
        self.gui.mainloop()

