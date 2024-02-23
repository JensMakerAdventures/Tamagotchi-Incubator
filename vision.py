import numpy as np
import matplotlib.pyplot as plt

from time import sleep
from datetime import datetime

from skimage import data
from skimage.feature import match_template
import skimage as ski
from skimage.transform import rescale

from skimage.io import imread
from skimage.io import imread_collection
from skimage import filters
import os

#os.environ.__setitem__('DISPLAY', ':0.0') 

class TamaVision(object):
    def __init__(self):
        
        dirName = 'sprites/*.png'
        self.positiveThreshold = 0.5 # value above this means we've found the pattern
        self.collection = imread_collection(dirName)
        #print(self.collection.files[0])

    def preProcess(self, imageFileName, patternFileName):
        pattern = ski.io.imread('sprites/' + patternFileName, as_gray=True)
        if patternFileName != 'needs_discipline.png':
            scaleFactor = 12.6 # scale value found through calibration, first step measure pixels, then trial and error test for best match
            print('ScaleFactor: ' + str(scaleFactor))
            pattern = rescale(pattern, scaleFactor, anti_aliasing = True, order=0) # nearest neighbour prevents blur

        image = ski.io.imread(imageFileName, as_gray=True)
        #thresh = filters.threshold_otsu(image)-0.38
        #print('Treshold: ' + str(thresh))
        #binary = image > thresh
       
        return image, pattern

    def findPattern(self, imageFileName, patternFileName):
        image, pattern = self.preProcess(imageFileName, patternFileName)

        result = match_template(image, pattern)
        ij = np.unravel_index(np.argmax(result), result.shape)
        x, y = ij[::-1]
        likeliness = result[ij]
        print('Likeliness template match: ' + str(likeliness))
        
        fig = plt.figure(figsize=(8, 3))
        now = datetime.now()
        current_time = datetime.datetime.now()
        #plt.title(current_time)
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

        plt.savefig('visionLog/' + current_time + '.png')
        
        if likeliness > self.positiveThreshold:
            plt.show()
        
        return (likeliness > self.positiveThreshold)

def testTamaVision():    
    tamaVision = TamaVision()
    tamaVision.findPattern('frame.jpg', 'angel.png')

#print("Running vision script!")
#testTamaVision()