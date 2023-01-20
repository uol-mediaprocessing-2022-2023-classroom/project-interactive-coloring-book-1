from skimage.segmentation import slic, mark_boundaries
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage.color import label2rgb
import cv2


img = mpimg.imread('mountainsNewK1.jpg')







# Applying SLIC segmentation
img_segments = slic(img,
						n_segments=500,
						compactness=3)
src = label2rgb(img_segments, img, kind = 'avg')

mpimg.imsave('mountainsNewSlicc.jpg', src)

# Plotting the original image
plt.imshow(src)
plt.show()