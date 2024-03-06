import os
from tkinter import *
from PIL import ImageTk,Image

def checkSetDisplay():
    # check if display env variable is ok
    if os.environ.get('DISPLAY','') == '':
        #print('No $DISPLAY env variable, so using :0.0')
        os.environ.__setitem__('DISPLAY', ':0.0')

class TamaGui():
    def __init__(self, buttonControllerInput):
        checkSetDisplay()
        self.buttonController = buttonControllerInput
        self.gui = Tk()
        self.gui.attributes('-fullscreen',True)
        self.gui.title("Tamagotchi-Incubator")
        self.buildGUI()

        self.autoMode = False
        self.loveMode = True

    def setAutoMode(self):
        self.autoMode = True

    def setManualMode(self):
        self.autoMode = False

    def setLoveMode(self):
        self.loveMode = True

    def setMurderMode(self):
        self.loveMode = False
        
    def buildGUI(self):
        fontSmall= ('Helvetica 26')
        fontBig = ('Helvetica 40')
        lButton = Button(self.gui, text ="Push L", command = self.buttonController.pressL, font = fontSmall)
        lButton.place(x=10,y=380)

        mButton = Button(self.gui, text ="Push M", command = self.buttonController.pressM, font = fontSmall)
        mButton.place(x=140,y=380)

        rButton = Button(self.gui, text ="Push R", command = self.buttonController.pressR, font = fontSmall)
        rButton.place(x=280,y=380)

        lAndRButton = Button(self.gui, text ="Push L&R", command = self.buttonController.pressLandR, font = fontSmall)
        lAndRButton.place(x=420,y=380)

        bAutoMode = Button(self.gui, text ="AUTOMATIC", command = self.setAutoMode, font = fontBig)
        bAutoMode.place(x=10,y=445)
        bManualMode = Button(self.gui, text ="MANUAL", command = self.setManualMode, font = fontBig)
        bManualMode.place(x=360,y=445)
        
        bLoveMode = Button(self.gui, text ="LOVE", command = self.setLoveMode, font = fontBig)
        bLoveMode.place(x=10,y=530)
        bManualMode = Button(self.gui, text ="MURDER", command = self.setMurderMode, font = fontBig)
        bManualMode.place(x=200,y=530)
        
    def update(self):
        imVision = Image.open('vision.png')
        w, h = imVision.size
        imVision = imVision.resize((int(w), int(h)))
        imVision = ImageTk.PhotoImage(imVision)
        label1 = Label(image=imVision)
        label1.place(x=500, y=20)
                
        imStats = Image.open('weight_age.jpg')
        w, h = imStats.size
        imStats = imStats.resize((int(w/3), int(h/3)))
        imStats = ImageTk.PhotoImage(imStats)
        label1 = Label(image=imStats)
        label1.place(x=800, y=20)

        imHungry = Image.open('hunger.jpg')
        w, h = imHungry.size
        imHungry = imHungry.resize((int(w/3), int(h/3)))
        imHungry = ImageTk.PhotoImage(imHungry)
        label1 = Label(image=imHungry)
        label1.place(x=800, y=200)

        imHappy = Image.open('happiness.jpg')
        w, h = imHappy.size
        imHappy = imHappy.resize((int(w/3), int(h/3)))
        imHappy = ImageTk.PhotoImage(imHappy)
        label1 = Label(image=imHappy)
        label1.place(x=800, y=380)

        imDiscipline = Image.open('discipline.jpg')
        w, h = imDiscipline.size
        imDiscipline = imDiscipline.resize((int(w/3), int(h/3)))
        imDiscipline = ImageTk.PhotoImage(imDiscipline)
        label1 = Label(image=imDiscipline)
        label1.place(x=800, y=560)


        self.gui.update()