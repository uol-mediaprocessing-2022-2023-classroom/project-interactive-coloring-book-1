import argparse

import cv2
import numpy as np
import cv2 as cv
from skimage.segmentation import slic, mark_boundaries


img = cv.imread('mountainsSLICResult.png')



img = cv2.GaussianBlur(img,(11,11),0)



print(img.size)
Z = img.reshape((-1, 3))
# convert to np.float32
Z = np.float32(Z)
# define criteria, number of clusters(K) and apply kmeans()
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 12
ret, label, center = cv.kmeans(Z, K, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)

print(center)

# Now convert back into uint8, and make original image
center = np.uint8(center)
res = center[label.flatten()]
src = res.reshape((img.shape))

scale_percent = 50

#calculate the 50 percent of original dimensions
width = int(src.shape[1] * scale_percent / 100)
height = int(src.shape[0] * scale_percent / 100)

# dsize
dsize = (width, height)
cv.imwrite("mountainsResultat.png", src)
# resize image
output = cv2.resize(src, dsize)
cv.imshow('res2', output)
cv.waitKey(0)
cv.destroyAllWindows()