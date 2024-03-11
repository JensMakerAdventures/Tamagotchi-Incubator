import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib

from time import sleep
from datetime import datetime

from skimage import data, exposure, feature
from skimage.feature import match_template
import skimage as ski
from skimage.transform import rescale
from skimage.filters import threshold_yen

from skimage.io import imread
import os

import shutil
import math
import logging

logger = logging.getLogger('Tamagotchi')

class TamaVision(object):
    def __init__(self, positiveThreshold, thresOffset, showResult, lock):
        self.thresOffset = thresOffset 
        self.positiveThreshold = positiveThreshold
        self.showResult = showResult
        self.lock = lock
        if showResult:
            matplotlib.use('TkAgg')
        else:
            matplotlib.use('agg')

        self.excludeImages = ['adult', 'teen', 'child', 'baby', 'egg', 'heart', 'angel', 'asleep', 'sleep_screen']
        
    
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
        for i in range(4):
            if self.findPattern(imageFileName, patternFileName, onlyCheckThisQuarter = (4-i)): #work from right to left until we find no more hearts missing
                missingHearts = missingHearts + 1
            else:
                return missingHearts
        return missingHearts
    
    def cropImage(self, image):
        return image[120:370, 95:570]
    
    def mealSelected(self, fn):
        input = ski.io.imread(fn, as_gray=True)
        cropped = self.cropImage(input) # crop screen
        thresh = threshold_yen(cropped)
        thresd = cropped > (thresh+self.thresOffset)
        selected = thresd[0:130, 0:100] # crop to arrow position for snack selection
        ''' # if you run below, you will be too late to select the right option...
        
        fig = plt.figure(figsize=(5, 3))
        ax1 = plt.subplot(1,4,1)
        ax1.imshow(input, cmap=plt.cm.gray)
        ax2 = plt.subplot(1,4,2)
        ax2.imshow(cropped, cmap=plt.cm.gray)
        ax3 = plt.subplot(1,4,3)
        ax3.imshow(thresd, cmap=plt.cm.gray)
        ax3 = plt.subplot(1,4,4)
        ax3.imshow(selected, cmap=plt.cm.gray)
        plt.savefig('smalldick.png', bbox_inches = 'tight', pad_inches = 0)
        '''
        avg = np.average(selected)
        #print(avg)
        if avg <0.85:
            logger.log(logging.WARNING,('Vision: Meal food option seems selected.'))
            return True
        else:
            logger.log(logging.WARNING,('Vision: Snack food option seems selected.'))
            return False


    def findPattern(self, imageFileName, patternFileNames, positiveThresholds = None, onlyCheckThisQuarter = 0):
        if not isinstance(patternFileNames, (tuple, list)):
            patternFileNames = [patternFileNames]
        if positiveThresholds is None:
            positiveThresholds = self.positiveThreshold
        if not isinstance(positiveThresholds, (tuple, list)):
            positiveThresholds = [positiveThresholds]

        for idx, patName in enumerate(patternFileNames):
            image = ski.io.imread(imageFileName, as_gray=True)

            if patName not in ['needs_discipline.png']:
                # crop image
                image = self.cropImage(image)

                # threshold image using yen algorithm, this is best (determined through try_all_threshold function from skimage)
                thresh = threshold_yen(image)
                image = image > (thresh+self.thresOffset)

            i = onlyCheckThisQuarter
            if i > 0:
                shape = np.shape(image)
                width = shape[1]
                quarter = math.floor(width/4)
                min = ((i-1)*quarter)
                max = i*quarter
                min = int(min - 0.21 * quarter) # compensate for not perfect quarters
                if min < 0:
                    min = 0
                max = int(max + 0.21 * quarter)
                if max > width:
                    max = width
                image = image[:, min:max]

            rescaleLive = False
            if rescaleLive:
                pattern = ski.io.imread('sprites/' + patName, as_gray=True) 
                scaleFactor = 12.6
                print('ScaleFactor: ' + str(scaleFactor))
                pattern = rescale(pattern, scaleFactor, anti_aliasing = True, order=0)      
            else:
                pattern = ski.io.imread('spritesRescaled/' + patName, as_gray=True)                                                                                              

            result = match_template(image, pattern)

            ij = np.unravel_index(np.argmax(result), result.shape)
            x, y = ij[::-1]
            likeliness = result[ij]
            
            fig = plt.figure(figsize=(5, 3))
            gs = GridSpec(3, 1, height_ratios=[1, 2, 2], hspace=0.3) 
            ax1 = plt.subplot(gs[0])
            ax2 = plt.subplot(gs[1])
            ax3 = plt.subplot(gs[2], sharex=ax2, sharey=ax2)

            ax1.set_anchor('C')
            ax2.set_anchor('C')
            ax3.set_anchor('C')

            ax1.imshow(pattern, cmap=plt.cm.gray)
            ax1.set_axis_off()
            ax1.set_title('Template: ' + patName)

            ax2.imshow(image, cmap=plt.cm.gray)
            ax2.set_axis_off()
            ax2.set_title('Screen frame')
            # highlight matched region
            htemplate, wtemplate = pattern.shape
            rect = plt.Rectangle((x, y), wtemplate, htemplate, edgecolor='r', facecolor='none')
            ax2.add_patch(rect)

            pShape = np.shape(pattern)
            width = pShape[1]
            height = pShape[0]
            halfWidth = int(width/2)
            halfHeight = int(height/2)
            padResult = np.pad(result, [(halfHeight, halfHeight), (halfWidth, halfWidth)], mode = 'constant', constant_values = 0)
            ax3.imshow(padResult)
            ax3.set_axis_off()
            ax3.set_title('Likeliness: ' + str(int(likeliness*100)) + '%')
            # highlight matched region
            ax3.autoscale(False)
            ax3.plot(x+halfWidth, y+halfHeight, 'o', markeredgecolor='r', markerfacecolor='none', markersize=10)

            now = datetime.now()
            date_time = now.strftime("%Y-%m-%d %H:%M:%S")

            # remove margins and whitespace, somehow this needs so much code
            plt.gca().set_axis_off()
            plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
            hspace = 0, wspace = 0)
            plt.margins(0,0)
            plt.gca().xaxis.set_major_locator(plt.NullLocator())
            plt.gca().yaxis.set_major_locator(plt.NullLocator())

            fn = 'vision.png'
            with self.lock:
                plt.savefig(fn, bbox_inches = 'tight', pad_inches = 0)

            if len(positiveThresholds) > 1:
                thres = positiveThresholds[idx]
            else:
                thres = positiveThresholds[0]

            #logger.log(logging.WARNING,('\nChecking pattern: ' + patName))
            #logger.log(logging.WARNING,'Likeliness template match: ' + "{:.2f}".format(likeliness))

            if likeliness > thres:
                if patName not in ['heart_empty.png']:
                    logger.log(logging.WARNING,(patName + ' found with ' + str(int(likeliness*100)) + '% likeliness'))
                if self.showResult:
                    plt.pause(10)               
                with self.lock:
                    shutil.copy(fn, 'visionLog/Found/' + date_time + patName) 
                plt.close()  
                if not any(ele in patName for ele in self.excludeImages):
                    shutil.copy(fn, 'visionLog/Interesting/' + date_time + patName) 
                return True
            else:
                with self.lock:
                    shutil.copy(fn, 'visionLog/NotFound/' + date_time + patName)
                plt.close()
        return False   

