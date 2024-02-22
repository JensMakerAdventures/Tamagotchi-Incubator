import numpy as np
import matplotlib.pyplot as plt

from time import sleep

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
        self.collection = imread_collection(dirName)
        #print(self.collection.files[0])

    def preProcess(self, imageFileName, patternFileName):
        pattern = ski.io.imread('sprites/' + patternFileName, as_gray=True)

        pattern = rescale(pattern, 15, anti_aliasing = True, order=0) # nearest neighbour prevents blur, scale value found through calibration, first step measure pixels, then trial and error test for best match
        
        image = ski.io.imread(imageFileName, as_gray=True)
        #thresh = filters.threshold_otsu(image)
        #print(thresh)
        binary = image# > 0.8
       
        return binary, pattern

    def findPattern(self, imageFileName, patternFileName):
        image, pattern = self.preProcess(imageFileName, patternFileName)

        result = match_template(image, pattern)
        ij = np.unravel_index(np.argmax(result), result.shape)
        x, y = ij[::-1]
        likeliness = result[ij]
        print('Likeliness template match: ' + str(likeliness))
        
        fig = plt.figure(figsize=(8, 3))
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

        plt.show()
        return likeliness

def testTamaVision():    
    tamaVision = TamaVision()
    tamaVision.findPattern('frame.jpg', 'angel.png')

#print("Running vision script!")
#testTamaVision()