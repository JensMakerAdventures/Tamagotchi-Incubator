import numpy as np
import matplotlib.pyplot as plt

from skimage import data
from skimage.feature import match_template
import skimage as ski

from skimage.io import imread
from skimage.io import imread_collection

class TamaVision(object):
    def __init__(self):
        
        dirName = '/*.png'
        collection = imread_collection(dirName)

def findPattern(image, pattern):
    if(pattern=='poop'):
        patternColor = ski.io.imread('poop.jpg')      
    else:
        return 0
    image = ski.color.rgb2gray(image)
    pattern = ski.color.rgb2gray(pattern)
    result = match_template(image, pattern)
    ij = np.unravel_index(np.argmax(result), result.shape)
    x, y = ij[::-1]
    likeliness = result[ij]
    
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
    return 

imageColor = ski.io.imread('test.jpg')
patternColor = ski.io.imread('poop.jpg')
findPattern(imageColor, patternColor)