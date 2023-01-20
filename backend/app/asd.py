from PIL import Image

# Opening the primary image (used in background)
img1 = Image.open("flowerNewK1.jpg")

# Opening the secondary image (overlay image)
img2 = Image.open("transparent_image.png")

# Pasting img2 image on top of img1
# starting at coordinates (0, 0)
img1.paste(img2, (0,0), mask = img2)

img1.save("pic.png")




