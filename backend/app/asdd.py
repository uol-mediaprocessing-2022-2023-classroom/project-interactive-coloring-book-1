from PIL import Image
import cv2


img = Image.open('mountainsSLIC.png')

rgba = img.convert("RGBA")
datas = rgba.getdata()

newData = []
for item in datas:
	if item[0] == 0 and item[1] == 0 and item[2] == 0: # finding black colour by its RGB value
		# storing a transparent value when we find a black colour
		newData.append((255, 255, 255, 0))
	else:
		newData.append(item) # other colours remain unchanged

rgba.putdata(newData)
rgba.save("transparent_image.png", "PNG")

# Opening the primary image (used in background)
img1 = Image.open("mountainsK1.png")

# Opening the secondary image (overlay image)
img2 = Image.open("transparent_image.png")

# Pasting img2 image on top of img1
# starting at coordinates (0, 0)
img1.paste(img2, (0,0), mask = img2)

img1.save("mountainsSLICResult.png")
