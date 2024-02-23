import numpy as np
import matplotlib.pyplot as plt

from time import sleep
from datetime import datetime

from skimage import data, exposure, feature
from skimage.feature import match_template
import skimage as ski
from skimage.transform import rescale

from skimage.io import imread
import os

from skimage.morphology import reconstruction
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
from skimage import data
from skimage.filters import threshold_yen
from skimage.filters import try_all_threshold

os.environ.__setitem__('DISPLAY', ':0.0') 


th = image > 0.6

imageFileName = 'frame.jpg'
image = ski.io.imread(imageFileName, as_gray=True)
image = image[134:341, 99:547]

thresh = threshold_yen(image)
binary = image > thresh


percentiles = np.percentile(image, (10, 30))
scaled = exposure.rescale_intensity(image, in_range=tuple(percentiles))
fig = plt.figure(figsize=(8, 3))
ax1 = plt.subplot(1, 3, 1)
ax1.imshow(binary, cmap=plt.cm.gray)
plt.pause(5)
plt.close()

#fig, ax = try_all_threshold(image, figsize=(10, 8), verbose=False)
#plt.show()
