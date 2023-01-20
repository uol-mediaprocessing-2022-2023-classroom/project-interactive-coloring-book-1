import matplotlib.pyplot as plt

import cv2 as cv
from skimage import segmentation
import matplotlib.image as mpimg
from skimage.color import label2rgb
from skimage.segmentation import slic

# Input data
img = mpimg.imread('testK1.png')

print(img.shape)


mask = mpimg.imread('testClosedMask.png')

print(mask.shape)


m_slic = segmentation.slic(img, n_segments=1000, mask=mask, compactness=1)



src = label2rgb(m_slic, img, kind = 'avg')

mpimg.imsave("testSLIC.png", src)


