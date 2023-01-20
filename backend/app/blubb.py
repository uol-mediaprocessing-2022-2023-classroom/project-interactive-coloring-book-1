import cv2
import numpy as np
import matplotlib.image as mpimg
from matplotlib import pyplot as plt

img = cv2.imread("testMask.png", cv2.IMREAD_UNCHANGED)
print(img.shape)

mask = img

kernel = np.ones((5,5), np.uint8)


opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
print(opening.shape)

cv2.imwrite("testClosedMask.png", opening)



# Display the Binary Image
cv2.imshow("Binary Image", closing)
cv2.waitKey(0)
cv2.destroyAllWindows()