from picamera import PiCamera
from time import sleep
import os
import matplotlib.pyplot as plt
import skimage as ski
from skimage.io import imread

'''
python3.9
from picamera import PiCamera
cam = PiCamera()
cam.start_preview()
'''

class TamaCam():
    def __init__(self):
        self.camera = PiCamera()
        self.setup()

    def setup(self):
        self.camera.zoom = (0.36, 0.19, 0.3, 0.3) #values found through calibration, in our case width and height size MUST be 0.3, or recalibrate pixel sizes too for vision
        self.camera.resolution = 'vga'
        #self.camera.framerate = 2
        self.camera.framerate = 5
        #self.camera.shutter_speed = 212339
        self.camera.shutter_speed = 200000
        self.camera.saturation = -100
        self.camera.brightness = 80
        self.camera.contrast = 100
        self.camera.sharpness = 100
        self.camera.video_denoise = 'False'

        # bug in camera, where it only correctly applies settings when taking frame, so take frame here
        self.getFrameToFile('a.jpg')
        os.remove('a.jpg')
        sleep(1) #to stabilize camera driver

    def getFrameToFile(self, filename):
        self.camera.capture(filename)

    def calibrate(self):
        self.camera.zoom = (0.01, 0.01, 0.99, 0.99) 
        self.getFrameToFile('fullFrame.jpg')
        self.getFrameToFile('fullFrame.jpg')
        self.getFrameToFile('fullFrame.jpg')
        self.getFrameToFile('fullFrame.jpg') # first 3 fail somehow
        self.camera.zoom = self.custom_crop
        self.getFrameToFile('cropFrame.jpg') #succeeds instantly somehow
        fig = plt.figure(figsize=(8, 3))

        fullFrame = ski.io.imread('fullFrame.jpg')
        cropFrame = ski.io.imread('cropFrame.jpg')

        ax1 = plt.subplot(1, 2, 1)
        ax1.set_title('Full camera frame')
        ax1.imshow(fullFrame)

        ax2 = plt.subplot(1, 2, 2)
        ax2.set_title('Using this crop')
        ax2.imshow(cropFrame)

        plt.show()
    
    def preview(self):
        self.camera.start_preview(fullscreen=False, window = (10, -140, 480, 640))