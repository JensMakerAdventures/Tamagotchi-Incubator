import vision
import os
import threading

lock = threading.Lock()

print("Running vision script!")
os.environ.__setitem__('DISPLAY', ':0.0') 

tamaVision = vision.TamaVision(0.4, 0.02, True, lock)
tamaVision.findPattern('frame.jpg', 'baby_2.png')
#tamaVision.findMissingHearts('hunger.jpg', 'heart_empty.png')
#tamaVision.findMissingHearts('happiness.jpg', 'heart_empty.png')





'''
# rescale all, manually do this once if you change cam position, manually clear the folder first

tamaVision.rescaleSprites('sprites', 'spritesRescaled', 12.6)
'''