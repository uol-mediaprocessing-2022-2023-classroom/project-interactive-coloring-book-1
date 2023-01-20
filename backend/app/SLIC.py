
from skimage.segmentation import slic, mark_boundaries
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage.color import label2rgb
import cv2


img = mpimg.imread('mountains.jpg')

img = cv2.GaussianBlur(img,(5,5),0)
img = cv2.GaussianBlur(img,(5,5),0)
img = cv2.GaussianBlur(img,(5,5),0)
img = cv2.GaussianBlur(img,(5,5),0)
img = cv2.GaussianBlur(img,(5,5),0)
img = cv2.GaussianBlur(img,(5,5),0)
img = cv2.GaussianBlur(img,(5,5),0)
img = cv2.GaussianBlur(img,(5,5),0)
img = cv2.GaussianBlur(img,(5,5),0)


# Applying SLIC segmentation
img_segments = slic(img,
						n_segments=250,
						compactness=10)

plt.subplot(2, 2, 1)

# Plotting the original image
plt.imshow(img)

# Detecting boundaries for labels
plt.subplot(2, 2, 2)

# Plotting the output of marked_boundaries
# function i.e. the image with segmented boundaries
plt.imshow(mark_boundaries(img, img_segments, color=(0,0,0)))

plt.subplot(2, 2, 3)

#Converts a label image into and RGB color image for visualizing the labeled regions
plt.imshow(label2rgb(img_segments, img, kind = 'avg'))

plt.subplot(2, 2, 4)
plt.imshow(mark_boundaries(label2rgb(img_segments, img, kind = 'avg'), img_segments, color=(0,0,0)))

plt.show()
