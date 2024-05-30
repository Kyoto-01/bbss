import numpy
import cv2

from hsi import (
    HSI,
    HUE_MAX,
    SATURATION_MAX,
    INTENSITY_MAX
)


def create_hsi_mask(
    imgRGB: "cv2.Mat", 
    minHue: "float" = 0, 
    maxHue: "float" = HUE_MAX,
    minSaturation: "float" = 0,
    maxSaturation: "float" = SATURATION_MAX,
    minIntensity: "float" = 0,
    maxIntensity: "float" = INTENSITY_MAX,
    maskValue: "int" = 1
):
    mask = numpy.zeros(imgRGB.shape)
    hsiFilter = HSI(imgRGB)
    h, s, i = hsiFilter.convert_rgb_to_hsi()

    for r in range(h.shape[0]):
        for c in range(h.shape[1]):
            hueCheck = (minHue <= h[r, c] <= maxHue)
            hueCheck = hueCheck or \
                (maxHue <= h[r, c] <= minHue)

            saturationCheck = (minSaturation <= s[r, c] <= maxSaturation)
            saturationCheck = saturationCheck or \
                (maxSaturation <= s[r, c] <= minSaturation)

            intensityCheck = (minIntensity <= i[r, c] <= maxIntensity)
            intensityCheck = intensityCheck or \
                (maxIntensity <= i[r, c] <= minIntensity)

            if (hueCheck and saturationCheck and intensityCheck):
                mask[r, c] = maskValue  

    return mask


def segment_by_color(imgRGB, hueMask):
  imgSegmentada = imgRGB.copy()
  for channel in range(imgSegmentada.shape[2]):
    imgSegmentada[:,:,channel] = imgSegmentada[:,:,channel] * hueMask[:,:,0]

  return imgSegmentada


if __name__ == "__main__":

    imgRGB = cv2.imread("elfo_soldado_300dpi.jpg")
    imgRGB = imgRGB[:, :, [2, 1, 0]]
    imgRGB = cv2.resize(imgRGB, dsize=(int(imgRGB.shape[1] / 5), int(imgRGB.shape[0] / 5)))

    hueMask = create_hue_mask(imgRGB, 345, 60)
    imgSegmented = segment_by_color(imgRGB, hueMask)

    cv2.imwrite("hsi.jpg", imgSegmented)
    cv2.waitKey()
