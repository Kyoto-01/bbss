import numpy
import cv2

from hsi import (
    HSI,
    HUE_MAX,
    SATURATION_MAX,
    INTENSITY_MAX
)

if __name__ == "__main__":
    imgRGB = cv2.imread("elfo_soldado_150dpi_adjusted.jpg")
    imgRGB = imgRGB[:, :, [2, 1, 0]]
    imgRGB = cv2.resize(imgRGB, dsize=(int(imgRGB.shape[1] / 5), int(imgRGB.shape[0] / 5)))

    hsiFilter = HSI(imgRGB)

    redMask = hsiFilter.create_hsi_mask(
        minHue=180,
        maxHue=10,
        minIntensity=0,
        maxIntensity=255,
        minSaturation=0,
        maxSaturation=100
    )

    blueMask = hsiFilter.create_hsi_mask(
        minHue=210,
        maxHue=250,
        minIntensity=0,
        maxIntensity=255,
        minSaturation=0,
        maxSaturation=100
    )

    blackMask = hsiFilter.create_hsi_mask(
        minHue=0,
        maxHue=360,
        minIntensity=0,
        maxIntensity=100,
        minSaturation=0,
        maxSaturation=100
    )

    img = numpy.ones(imgRGB.shape) * 255
    img[redMask == 1] = [0, 0, 255]
    img[blueMask == 1] = [255, 0, 0]
    img[blackMask == 1] = [0, 0, 0]

    cv2.imwrite("hsi.bmp", img)
