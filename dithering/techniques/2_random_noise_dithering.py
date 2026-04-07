# take input image, convert to grayscale
# loop through every pixel
# for each pixel, choose a random threshold between 0 and 255
# if the pixel value is below the random threshold, set it to black (0)
# if the pixel value is above the random threshold, set it to white (255)

import random

from PIL import Image

inputImage = Image.open("./base_images/dp_scotland.png")

grayImage = inputImage.convert("L")

grayImagePixels = grayImage.load()
grayImageWidth, grayImageHeight = grayImage.size

outputImage = Image.new("L", (grayImageWidth, grayImageHeight))

for x in range(grayImageWidth):
    for y in range(grayImageHeight):
        pixelVal = grayImagePixels[x, y]
        randomThreshold = random.randint(0, 255)

        if pixelVal <= randomThreshold:
            outputImage.putpixel((x, y), 0)
        else:
            outputImage.putpixel((x, y), 255)

outputImage.save("./output_images/2_dp_scotland.png")
