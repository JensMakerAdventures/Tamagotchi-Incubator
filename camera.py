from picamera import PiCamera
from time import sleep

class TamaCam():
    def __init(self):
        self.camera = PiCamera()
        #self.camera.resolution = (800, 600)
        #self.camera.framerate = 15

    def getFrame(self):
        #camera.start_preview()
        #sleep(5)
        frame = self.camera.capture() #'test.jpg'
        #camera.stop_preview()
        return frame
    
    def preview(self, seconds):
        self.camaera.start_preview()
        sleep(seconds)
        self.camaera.stop_preview()