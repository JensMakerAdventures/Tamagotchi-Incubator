import numpy as np
import matplotlib.pyplot as plt

from time import sleep

from skimage import data
from skimage.feature import match_template
import skimage as ski
from skimage.transform import rescale

from skimage.io import imread
from skimage.io import imread_collection



class TamaVision(object):
    def __init__(self):
        
        dirName = 'sprites/*.png'
        self.collection = imread_collection(dirName)
        #print(self.collection.files[0])

    def findPattern(self, imageLocation, patternName):
        pattern = ski.io.imread('sprites/angel.png', as_gray=True)  
        pattern = rescale(pattern, 12.7, anti_aliasing = True)

        image = ski.io.imread(imageLocation, as_gray=True)   

        #image = ski.color.rgb2gray(imageImported)

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
        ax1.set_title('template')

        ax2.imshow(image, cmap=plt.cm.gray)
        ax2.set_axis_off()
        ax2.set_title('image')
        # highlight matched region
        htemplate, wtemplate = pattern.shape
        rect = plt.Rectangle((x, y), wtemplate, htemplate, edgecolor='r', facecolor='none')
        ax2.add_patch(rect)

        ax3.imshow(result)
        ax3.set_axis_off()
        ax3.set_title('`match_template`\nresult')
        # highlight matched region
        ax3.autoscale(False)
        ax3.plot(x, y, 'o', markeredgecolor='r', markerfacecolor='none', markersize=10)

        plt.show()
        sleep(100)
        return likeliness

def testTamaVision():    
    tamaVision = TamaVision()
    tamaVision.findPattern('frame.jpg', 'angel')

#testTamaVision()