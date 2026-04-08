# similar to floyd-steinberg, but only distributes 75% of error (throws 25% away)
# and uses different diffusion matrix
#
# take input image, convert to grayscale
# loop through every pixel
# (similar to thresholding)
# if the pixel value is below the midpoint threshold (127), set it to black (0)
# if the pixel value is above the midpoint threshold, set it to white (255)
# but note the quantization error (difference between original value and what we set it to)
# and distribute that error using this matrix:
# [0 0 * 1/8 1/8; 1/8 1/8 1/8 0 0; 0 0 1/8 0 0] where * is the current pixel

from PIL import Image

inputImage = Image.open("./base_images/dp_scotland.png")

grayImage = inputImage.convert("L")

grayImagePixels = grayImage.load()
grayImageWidth, grayImageHeight = grayImage.size

outputImage = Image.new("L", (grayImageWidth, grayImageHeight))

# note: had to swap to row-by-row for the error diffusion
for y in range(grayImageHeight):
    for x in range(grayImageWidth):
        pixelVal = grayImagePixels[x, y]

        if pixelVal <= 127:
            error = pixelVal - 0
            outputImage.putpixel((x, y), 0)
        else:
            error = pixelVal - 255
            outputImage.putpixel((x, y), 255)

        # distribute error to future pixels
        if x + 1 < grayImageWidth:
            grayImagePixels[x + 1, y] = int(grayImagePixels[x + 1, y] + (error * 1 / 8))

        if x - 1 >= 0 and y + 1 < grayImageHeight:
            grayImagePixels[x - 1, y + 1] = int(
                grayImagePixels[x - 1, y + 1] + (error * 1 / 8)
            )

        if y + 1 < grayImageHeight:
            grayImagePixels[x, y + 1] = int(grayImagePixels[x, y + 1] + (error * 1 / 8))

        if x + 1 < grayImageWidth and y + 1 < grayImageHeight:
            grayImagePixels[x + 1, y + 1] = int(
                grayImagePixels[x + 1, y + 1] + (error * 1 / 8)
            )

        if x + 2 < grayImageWidth:
            grayImagePixels[x + 2, y] = int(grayImagePixels[x + 2, y] + (error * 1 / 8))

        if y + 2 < grayImageHeight:
            grayImagePixels[x, y + 2] = int(grayImagePixels[x, y + 2] + (error * 1 / 8))

outputImage.save("./output_images/5_dp_scotland.png")
