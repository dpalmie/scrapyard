# ordered dithering uses bayer matrices
#
# 2x2 bayer matrix is [0 2; 3 1]
# 4x4 bayer matrix is [0 8 2 10; 12 4 14 6; 3 11 1 9; 15 7 13 5]
# 8x8 bayer matrix is [
#   0 32 8 40 2 34 10 42;
#   48 16 56 24 50 18 58 26;
#   12 44 4 36 14 46 6 38;
#   60 28 52 20 62 30 54 22;
#   3 35 11 43 1 33 9 41;
#   51 19 59 27 49 17 57 25;
#   15 47 7 39 13 45 5 37;
#   63 31 55 23 61 29 53 21
# ]
# (bayer matrices are only defined for dimensions that are powers of 2)
#
# how are bayer matrices made?
# TODO
#
# and we need to scale largest matrix value to 255
# use formula: multiplier = highest val / (matrix_row_or_col_count_n ^2 - 1)
# which is:
#   2x2 -> 255 / (2^2 - 1) -> 85
#   4x4 -> 255 / (4^2 - 1) -> 17
#   8x8 -> 255 / (8^2 - 1) -> 4.05
# so for:
#   2x2 -> multiply everything by 85 -> new matrix is [0 170; 255 85]
#   4x4 -> multiply everything by 17 -> new matrix is
#          [0 136 34 170; 204 68 238 102; 51 187 17 153; 255 119 221 85]
#   8x8 -> multiply everything by 4.05 -> new matrix is
#   [
#     0 130 32 162 8 138 40 170;
#     194 65 227 97 202 73 235 105;
#     49 178 16 146 57 186 24 154;
#     243 113 210 81 251 121 219 89;
#     12 142 45 174 4 134 36 166;
#     206 77 239 109 198 69 231 101;
#     61 190 28 158 53 182 20 150;
#     255 125 223 93 247 117 215 85
#  ]
#
# now:
# take input image, convert to grayscale
# loop the matrix across the image
# find what matrix cell applies to current pixel
# use scaled matrix value for threshold:
#   if above -> set it to white (255)
#   if below -> set it to black (0)

from PIL import Image

bayerMatrix2x2 = [[0, 170], [255, 85]]
bayerMatrix4x4 = [
    [0, 136, 34, 170],
    [204, 68, 238, 102],
    [51, 187, 17, 153],
    [255, 119, 221, 85],
]
bayerMatrix8x8 = [
    [0, 130, 32, 162, 8, 138, 40, 170],
    [194, 65, 227, 97, 202, 73, 235, 105],
    [49, 178, 16, 146, 57, 186, 24, 154],
    [243, 113, 210, 81, 251, 121, 219, 89],
    [12, 142, 45, 174, 4, 134, 36, 166],
    [206, 77, 239, 109, 198, 69, 231, 101],
    [61, 190, 28, 158, 53, 182, 20, 150],
    [255, 125, 223, 93, 247, 117, 215, 85],
]

inputImage = Image.open("./base_images/dp_scotland.png")

grayImage = inputImage.convert("L")

grayImagePixels = grayImage.load()
grayImageWidth, grayImageHeight = grayImage.size

outputImage2x2 = Image.new("L", (grayImageWidth, grayImageHeight))
outputImage4x4 = Image.new("L", (grayImageWidth, grayImageHeight))
outputImage8x8 = Image.new("L", (grayImageWidth, grayImageHeight))

for x in range(grayImageWidth):
    for y in range(grayImageHeight):
        pixelVal = grayImagePixels[x, y]

        # 2x2 matrix ordered dithering
        matrix2x2RowVal = x % 2
        matrix2x2ColVal = y % 2

        matrix2x2ThresholdVal = bayerMatrix2x2[matrix2x2RowVal][matrix2x2ColVal]

        if pixelVal <= matrix2x2ThresholdVal:
            outputImage2x2.putpixel((x, y), 0)
        else:
            outputImage2x2.putpixel((x, y), 255)

        # 4x4 matrix ordered dithering
        matrix4x4RowVal = x % 4
        matrix4x4ColVal = y % 4

        matrix4x4ThresholdVal = bayerMatrix4x4[matrix4x4RowVal][matrix4x4ColVal]

        if pixelVal <= matrix4x4ThresholdVal:
            outputImage4x4.putpixel((x, y), 0)
        else:
            outputImage4x4.putpixel((x, y), 255)

        # 8x8 matrix ordered dithering
        matrix8x8RowVal = x % 8
        matrix8x8ColVal = y % 8

        matrix8x8ThresholdVal = bayerMatrix8x8[matrix8x8RowVal][matrix8x8ColVal]

        if pixelVal <= matrix8x8ThresholdVal:
            outputImage8x8.putpixel((x, y), 0)
        else:
            outputImage8x8.putpixel((x, y), 255)

outputImage2x2.save("./output_images/3_2x2_dp_scotland.png")
outputImage4x4.save("./output_images/3_4x4_dp_scotland.png")
outputImage8x8.save("./output_images/3_8x8_dp_scotland.png")
