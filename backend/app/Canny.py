import cv2
from skimage import util

img = cv2.imread("flowerNewK1.jpg")  # Read image

# Setting parameter values
t_lower = 25  # Lower Threshold
t_upper = 100  # Upper threshold

# Applying the Canny Edge filter
edge = cv2.Canny(img, t_lower, t_upper)
edge = util.invert(edge)

cv2.imwrite("flowerCanny.jpg", edge)

cv2.imshow('original', img)
cv2.imshow('edge', edge)
cv2.waitKey(0)
cv2.destroyAllWindows()