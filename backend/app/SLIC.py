# Importing required boundaries
from skimage.segmentation import slic, mark_boundaries
from skimage.data import astronaut
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage.color import label2rgb
from PIL import Image


image = Image.open('flower.jpg')
image = image.resize((int(image.size[0]/3),int(image.size[1]/3)))
image.save('newFlower.jpg')
# Setting the plot figure as 15, 15
plt.figure(figsize=(15, 15))


img = mpimg.imread('newFlower.jpg')

# Applying SLIC segmentation
img_segments = slic(img,
						n_segments=500,
						compactness=10)

plt.subplot(2, 2, 1)

# Plotting the original image
plt.imshow(img)

# Detecting boundaries for labels
plt.subplot(2, 2, 2)

# Plotting the output of marked_boundaries
# function i.e. the image with segmented boundaries
plt.imshow(mark_boundaries(img, img_segments))

plt.subplot(2, 2, 3)

#Converts a label image into and RGB color image for visualizing the labeled regions
plt.imshow(label2rgb(img_segments, img, kind = 'avg'))

plt.subplot(2, 2, 4)
plt.imshow(mark_boundaries(label2rgb(img_segments, img, kind = 'avg'), img_segments))

plt.show()
