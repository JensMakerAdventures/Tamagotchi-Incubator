import vision
import os

print("Running vision script!")
os.environ.__setitem__('DISPLAY', ':0.0') 
tamaVision = vision.TamaVision()
tamaVision.findPattern('frame.jpg', 'child.png')




'''
# rescale all, manually do this once if you change cam position, manually clear the folder first
import vision
vis = vision.TamaVision()
vis.rescaleSprites('sprites', 'spritesRescaled', 12.6)
'''