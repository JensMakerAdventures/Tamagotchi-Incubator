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




imageFileName = 'frame.jpg'
image = ski.io.imread(imageFileName, as_gray=True)
image = image[110:341, 95:570]
fig, ax = try_all_threshold(image, figsize=(10, 8), verbose=False)
plt.show()

th = image > 0.6

thresh = threshold_yen(image)
binary = image > thresh


percentiles = np.percentile(image, (10, 30))
scaled = exposure.rescale_intensity(image, in_range=tuple(percentiles))
fig = plt.figure(figsize=(8, 3))
ax1 = plt.subplot(1, 3, 1)
ax1.imshow(binary, cmap=plt.cm.gray)
plt.pause(5)
plt.close()



import numpy as np
from scipy import ndimage as ndi
from matplotlib import pyplot as plt
import matplotlib.cm as cm

from skimage import data
from skimage import color
from skimage.util import view_as_blocks
from skimage.filters import threshold_yen

import os
os.environ.__setitem__('DISPLAY', ':0.0') 


# get astronaut from skimage.data in grayscale
imageFileName = 'frame.jpg'
import skimage as ski
image = ski.io.imread(imageFileName, as_gray=True)
l = image # = color.rgb2gray(image)
l = l[134:341, 99:547]

# size of blocks
block_shape = (8, 4) #7.5, 3.8)

# see astronaut as a matrix of blocks (of shape block_shape)
view = view_as_blocks(l, block_shape)

# collapse the last two dimensions in one
flatten_view = view.reshape(view.shape[0], view.shape[1], -1)

# resampling the image by taking either the `mean`,
# the `max` or the `median` value of each blocks.
thresh = threshold_yen(image)

thresh_offset = -0.28

mean_view = np.mean(flatten_view, axis=2) > (thresh+thresh_offset)
max_view = np.max(flatten_view, axis=2) > (thresh+thresh_offset)
median_view = np.median(flatten_view, axis=2) > (thresh+thresh_offset)

# display resampled images
fig, axes = plt.subplots(2, 2, figsize=(8, 8), sharex=True, sharey=True)
ax = axes.ravel()

l_resized = ndi.zoom(l, 2, order=3)
ax[0].set_title("Original rescaled with\n spline interpolation (order=3)")
ax[0].imshow(l_resized, extent=(-0.5, 128.5, 128.5, -0.5),
             cmap=cm.Greys_r)

ax[1].set_title("Block view with\n local mean pooling")
ax[1].imshow(mean_view, cmap=cm.Greys_r)

ax[2].set_title("Block view with\n local max pooling")
ax[2].imshow(max_view, cmap=cm.Greys_r)

ax[3].set_title("Block view with\n local median pooling")
ax[3].imshow(median_view, cmap=cm.Greys_r)

for a in ax:
    a.set_axis_off()

fig.tight_layout()
plt.show()