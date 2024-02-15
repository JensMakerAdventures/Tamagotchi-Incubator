from picamera import PiCamera
from time import sleep
import os

class TamaCam():
    def __init__(self):
        self.camera = PiCamera()
        self.setup()

    def setup(self):
        self.camera.resolution = 'vga'
        self.camera.framerate = 2
        self.camera.shutter_speed = 300000
        self.camera.saturation = -100
        self.camera.zoom = (0.32, 0.25, 0.3, 0.3)
        self.camera.brightness = 60
        self.camera.contrast = 100
        self.camera.sharpness = 100
        self.camera.video_denoise = 'False'

        # bug in camera, where it only correctly applies settings when taking frame, so take frame here
        self.getFrameToFile('a.jpg')
        os.remove('a.jpg')


    def getFrameToFile(self, filename):
        self.camera.capture(filename)
    
    def preview(self, seconds):
        self.camera.start_preview()
        sleep(seconds)
        self.camera.stop_preview()
