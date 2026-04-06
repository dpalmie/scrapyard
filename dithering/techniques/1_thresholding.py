# take input image, convert to grayscale
# loop through every pixel
# if the pixel value is below the midpoint threshold (127), set it to black (0)
# if the pixel value is above the midpoint threshold, set it to white (255)

from PIL import Image

inputImage = Image.open("./base_images/dp_scotland.png")

grayImage = inputImage.convert("L")

grayImagePixels = grayImage.load()
grayImageWidth, grayImageHeight = grayImage.size

outputImage = Image.new("L", (grayImageWidth, grayImageHeight))

for x in range(grayImageWidth):
    for y in range(grayImageHeight):
        pixelVal = grayImagePixels[x, y]
        # print(pixelVal)
        if pixelVal <= 127:
            outputImage.putpixel((x, y), 0)
        else:
            outputImage.putpixel((x, y), 255)

outputImage.save("./output_images/1_dp_scotland.png")
