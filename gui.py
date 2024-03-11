import os
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from PIL import ImageTk,Image
from time import sleep
import QueueHandler
import logging
import queue
import os


logger = logging.getLogger('Tamagotchi')

def checkSetDisplay():
    # check if display env variable is ok
    if os.environ.get('DISPLAY','') == '':
        #print('No $DISPLAY env variable, so using :0.0')
        os.environ.__setitem__('DISPLAY', ':0.0')

class TamaGui():
    def __init__(self, buttonControllerInput, lightController, lock):
        checkSetDisplay()
        self.buttonController = buttonControllerInput
        self.gui = Tk()
        self.gui.attributes('-fullscreen',True)
        self.gui.title("Tamagotchi-Incubator")
        self.lock = lock
        self.lightController = lightController
        self.DefClr = self.gui.cget("bg")
        self.autoMode = False
        self.loveMode = True

        self.buildGUI()

    def setAutoMode(self):
        self.autoMode = True

    def setManualMode(self):
        self.autoMode = False

    def setLoveMode(self):
        self.loveMode = True

    def setMurderMode(self):
        self.loveMode = False

    def shutdown(self):
        os.system('sudo shutdown -r now')
        
    def stop_app(self):
        exit()

    def buildGUI(self):
        fontLog= ('Helvetica 20')
        fontSmall= ('Helvetica 26')
        fontBig = ('Helvetica 40')
        lButton = Button(self.gui, text ="Push L", command = self.buttonController.pressL, font = fontSmall)
        lButton.place(x=10,y=370)

        mButton = Button(self.gui, text ="Push M", command = self.buttonController.pressM, font = fontSmall)
        mButton.place(x=140,y=370)

        lightOnButton = Button(self.gui, text ="Light On", command = self.lightController.turnOn, font = fontSmall)
        lightOnButton.place(x=610,y=370)

        lightOffButton = Button(self.gui, text ="Light Off", command = self.lightController.turnOff, font = fontSmall)
        lightOffButton.place(x=610,y=420)

        shutdownButton = Button(self.gui, text ="Shutdown", command = self.shutdown, font = fontSmall)
        shutdownButton.place(x=610,y=470)

        restartButton = Button(self.gui, text ="Stop app", command = self.stop_app, font = fontSmall)
        restartButton.place(x=610,y=520)

        rButton = Button(self.gui, text ="Push R", command = self.buttonController.pressR, font = fontSmall)
        rButton.place(x=280,y=370)

        lAndRButton = Button(self.gui, text ="Push L&R", command = self.buttonController.pressLandR, font = fontSmall)
        lAndRButton.place(x=420,y=370)

        self.bAutoMode = Button(self.gui, text ="AUTOMATIC", command = self.setAutoMode, font = fontBig)
        self.bAutoMode.place(x=10,y=425)
        self.bManualMode = Button(self.gui, text ="MANUAL", command = self.setManualMode, font = fontBig)
        self.bManualMode.place(x=360,y=425)
        
        self.bLoveMode = Button(self.gui, text ="LOVE", command = self.setLoveMode, font = fontBig)
        self.bLoveMode.place(x=10,y=500)
        self.bMurderMode = Button(self.gui, text ="MURDER", command = self.setMurderMode, font = fontBig)
        self.bMurderMode.place(x=200,y=500)

        lVision = Label()
        lVision.place(x=500, y=20)
        lStats = Label()
        lStats.place(x=800, y=20)
        lHungry = Label()
        lHungry.place(x=800, y=200)
        lHappy = Label()
        lHappy.place(x=800, y=380)
        lDiscipline = Label()
        lDiscipline.place(x=800, y=560)

        self.text_widget = Text(self.gui, wrap="word", width=41, height=7, font = fontLog)
        self.text_widget.place(x=10, y=570)

        # format: label object, filename, scale x, scale y
        self.images = ((lVision, 'vision.png', 1, 1), 
                       (lStats, 'weight_age.jpg', 0.33, 0.33),
                       (lHungry, 'hunger.jpg', 0.33, 0.33),
                       (lHappy, 'happiness.jpg', 0.33, 0.33),
                       (lDiscipline, 'discipline.jpg', 0.33, 0.33),
        )

        # Create a logging handler using a queue
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler.QueueHandler(self.log_queue)
        formatter = logging.Formatter('%(message)s')
        self.queue_handler.setFormatter(formatter)
        logger.addHandler(self.queue_handler)
        # Start polling messages from the queue
        self.gui.after(100, self.poll_log_queue)


    def displayText(self, record):
        msg = self.queue_handler.format(record)
        self.text_widget.configure(state='normal')
        self.text_widget.insert(END, msg + '\n', record.levelname)
        self.text_widget.configure(state='disabled')
        # Autoscroll to the bottom
        self.text_widget.yview(END)

    def poll_log_queue(self):
        # Check every 100ms if there is a new message in the queue to display
        while True:
            try:
                record = self.log_queue.get(block=False)
            except queue.Empty:
                break
            else:
                self.displayText(record)
        self.gui.after(100, self.poll_log_queue)

    def updateContent(self):
        # update button colors
        if self.autoMode:
            self.bAutoMode.config(bg='green')
            self.bManualMode.config(bg=self.DefClr)
        else:
            self.bAutoMode.config(bg=self.DefClr)
            self.bManualMode.config(bg='red')

        if self.loveMode:
            self.bLoveMode.config(bg='green')
            self.bMurderMode.config(bg=self.DefClr)
        else:
            self.bLoveMode.config(bg=self.DefClr)
            self.bMurderMode.config(bg='red')

        # update images
        for image in self.images:
            fn = image[1]
            
            with self.lock:
                im = Image.open(fn)
            w, h = im.size
            im = im.resize((int(w*image[2]), int(h*image[3])))
            im = ImageTk.PhotoImage(im)
            image[0].configure(image = im)
            image[0].image = im # keep a reference!

        self.gui.after(300, self.updateContent)

    def mainloop(self):
        self.updateContent()
        self.gui.mainloop()