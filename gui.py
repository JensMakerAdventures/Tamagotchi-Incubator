import os
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from PIL import ImageTk,Image
from time import sleep
import fasteners
import QueueHandler
import logging
import queue

logger = logging.getLogger()

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

        self.text_widget = Text(self.gui, wrap="word", width=41, height=4, font = fontSmall)
        self.text_widget.place(x=10, y=610)

        # format: label object, filename, scale x, scale y
        self.images = ((lVision, 'vision.png', 1, 1), 
                       (lStats, 'weight_age.jpg', 0.33, 0.33),
                       (lHungry, 'hunger.jpg', 0.33, 0.33),
                       (lHappy, 'happiness.jpg', 0.33, 0.33),
                       (lDiscipline, 'discipline.jpg', 0.33, 0.33),
        )

        self.scrolled_text = ScrolledText(self.gui, state='disabled', height=12)
        self.scrolled_text.grid(row=0, column=0, sticky=(N, S, W, E))
        self.scrolled_text.configure(font='TkFixedFont')
        self.scrolled_text.tag_config('INFO', foreground='black')
        self.scrolled_text.tag_config('DEBUG', foreground='gray')
        self.scrolled_text.tag_config('WARNING', foreground='orange')
        self.scrolled_text.tag_config('ERROR', foreground='red')
        self.scrolled_text.tag_config('CRITICAL', foreground='red', underline=1)
        # Create a logging handler using a queue
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler.QueueHandler(self.log_queue)
        formatter = logging.Formatter('%(asctime)s: %(message)s')
        self.queue_handler.setFormatter(formatter)
        logger.addHandler(self.queue_handler)
        # Start polling messages from the queue
        self.gui.after(100, self.poll_log_queue)


    def displayText(self, record):
        msg = self.queue_handler.format(record)
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert(END, msg + '\n', record.levelname)
        self.scrolled_text.configure(state='disabled')
        # Autoscroll to the bottom
        self.scrolled_text.yview(END)

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
        # update images
        for image in self.images:
            fn = image[1]
            lock = fasteners.InterProcessLock(fn)
            with lock:
                im = Image.open(fn)
            w, h = im.size
            im = im.resize((int(w*image[2]), int(h*image[3])))
            im = ImageTk.PhotoImage(im)
            image[0].configure(image = im)
            image[0].image = im # keep a reference!
        '''
        # update text
        file_path=logging.getLoggerClass().root.handlers[0].baseFilename
        lock = fasteners.InterProcessLock(file_path)
        with lock:            
            with open(file_path, 'r') as file:
                content = file.readlines()
                content = content[-4:] 
                self.text_widget.delete(1.0, END)  # Clear previous content
                self.text_widget.insert(END, "".join(content))
        '''
        self.gui.after(1000, self.updateContent)

    def mainloop(self):
        self.updateContent()
        self.gui.mainloop()