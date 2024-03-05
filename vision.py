import numpy as np
import matplotlib.pyplot as plt

from time import sleep
from datetime import datetime

from skimage import data, exposure, feature
from skimage.feature import match_template
import skimage as ski
from skimage.transform import rescale
from skimage.filters import threshold_yen

from skimage.io import imread
import os

import math

class TamaVision(object):
    positiveThreshold = 0.40 # value above this means we've found the pattern
    def __init__(self):
        self.thresOffset = 0.02
        

    # 12.6x scale value found through calibration, first step measure pixels, then trial and error test for best match
    def rescaleSprites(self, spritesFolder, rescaledFolder, scaleFactor):
        for filename in os.listdir(spritesFolder):
            image = ski.io.imread(spritesFolder+'/'+filename, as_gray=True)

            
            if filename != ('needs_discipline.png'): #this one is straight captured from the display, doesn't need scaling
                image = rescale(image, scaleFactor, anti_aliasing = True, order=0) # nearest neighbour prevents blur
            image = ski.util.img_as_ubyte(image) # needed because otherwise trying to store floats between 0 and 1 in uint formatted png
            ski.io.imsave(rescaledFolder+'/'+filename, image)

    def findMissingHearts(self, imageFileName, patternFileName):
        missingHearts = 0
        for i in range(3):
            if self.findPattern(imageFileName, patternFileName, onlyCheckThisQuarter = (4-i)): #work from right to left until we find no more hearts missing
                missingHearts = missingHearts + 1
            else:
                return missingHearts
        return missingHearts


    def findPattern(self, imageFileName, patternFileName, positiveThreshold = positiveThreshold, onlyCheckThisQuarter = 0):
        image = ski.io.imread(imageFileName, as_gray=True)

        if patternFileName not in ['needs_discipline.png']:
            # crop image
            image = image[134:341, 99:547]

            # threshold image using yen algorithm, this is best (determined through try_all_threshold function from skimage)
            thresh = threshold_yen(image)
            image = image > (thresh+self.thresOffset)

        i = onlyCheckThisQuarter
        if onlyCheckThisQuarter > 0:
            shape = np.shape(image)
            width = shape[1]
            quarter = math.floor(width/4)
            image = image[:, ((i-1)*quarter):i*quarter]

        rescaleLive = False
        if rescaleLive:
            pattern = ski.io.imread('sprites/' + patternFileName, as_gray=True) 
            scaleFactor = 12.6
            print('ScaleFactor: ' + str(scaleFactor))
            pattern = rescale(pattern, scaleFactor, anti_aliasing = True, order=0)      
        else:
            pattern = ski.io.imread('spritesRescaled/' + patternFileName, as_gray=True)                                                                                              

        result = match_template(image, pattern)

        ij = np.unravel_index(np.argmax(result), result.shape)
        x, y = ij[::-1]
        likeliness = result[ij]
        print('\nChecking pattern: ' + patternFileName)
        print('Likeliness template match: ' + "{:.2f}".format(likeliness))
        
        fig = plt.figure(figsize=(30, 12))
        ax1 = plt.subplot(1, 3, 1)
        ax2 = plt.subplot(1, 3, 2)
        ax3 = plt.subplot(1, 3, 3, sharex=ax2, sharey=ax2)

        ax1.imshow(pattern, cmap=plt.cm.gray)
        ax1.set_axis_off()
        ax1.set_title('Template: ' + patternFileName)

        ax2.imshow(image, cmap=plt.cm.gray)
        ax2.set_axis_off()
        ax2.set_title('Screen frame')
        # highlight matched region
        htemplate, wtemplate = pattern.shape
        rect = plt.Rectangle((x, y), wtemplate, htemplate, edgecolor='r', facecolor='none')
        ax2.add_patch(rect)

        ax3.imshow(result)
        ax3.set_axis_off()
        ax3.set_title('Likeliness: ' + str(int(likeliness*100)) + '%')
        # highlight matched region
        ax3.autoscale(False)
        ax3.plot(x, y, 'o', markeredgecolor='r', markerfacecolor='none', markersize=10)

        mng = plt.get_current_fig_manager()
        mng.resize(*mng.window.maxsize())

        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        plt.savefig('visionLog/' + date_time + patternFileName)
        
        if patternFileName != 'needs_discipline.png':
            if likeliness > positiveThreshold:
                plt.pause(10)
            plt.close()
            
            return (likeliness > positiveThreshold)
        else:
            if likeliness > 0.85:
                plt.pause(10)
            plt.close()
            return (likeliness > 0.85)
            
        
        

def testTamaVision():    
    os.environ.__setitem__('DISPLAY', ':0.0') 
    tamaVision = TamaVision()
    tamaVision.findPattern('frame.jpg', 'child.png')


'''
# rescale all, manually do this once if you change cam position, manually clear the folder first
import vision
vis = vision.TamaVision()
vis.rescaleSprites('sprites', 'spritesRescaled', 12.6)
'''
#print("Running vision script!")
#testTamaVision()
    

