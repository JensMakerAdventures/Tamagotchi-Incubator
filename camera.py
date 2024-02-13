from picamera import PiCamera

def getFrame():
    camera = PiCamera()
    #camera.resolution = (800, 600)
    #camera.framerate = 15
    #camera.start_preview()
    #sleep(5)
    frame = camera.capture() #'test.jpg'
    #camera.stop_preview()
    return frame
