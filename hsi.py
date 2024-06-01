import numpy
import cv2


HUE_MAX = 180 / numpy.pi
SATURATION_MAX = 100
INTENSITY_MAX = 255


class HSI:

    def __init__(
        self, 
        imgRGB
    ):
        self.__chR = None
        self.__chG = None
        self.__chB = None

        self.__setup(imgRGB)

    def __setup(
        self, 
        imgRGB
    ):
        imgRGB = cv2.normalize(
            src=imgRGB, 
            dst=None, 
            alpha=0, 
            beta=1, 
            norm_type=cv2.NORM_MINMAX, 
            dtype=cv2.CV_32FC3
        )
        self.__chR, self.__chG, self.__chB = cv2.split(imgRGB)

    def calculate_hue(
        self
    ):
        numerator = 0.5
        numerator *= ((self.__chR - self.__chG) + (self.__chR - self.__chB))

        denominator = ((self.__chR - self.__chG)**2)
        denominator += ((self.__chR - self.__chB) * (self.__chG - self.__chB))
        denominator = numpy.sqrt(denominator)
        denominator[denominator == 0] = 1e-10

        hue = numpy.arccos(numerator / denominator)
        hue[self.__chB > self.__chG] = (
            ((360 * numpy.pi) / 180) - hue[self.__chB > self.__chG])
        hue = hue * HUE_MAX

        return hue
        
    def calculate_saturation(
        self
    ):
        sumRGB = (self.__chR + self.__chG + self.__chB)
        sumRGB[sumRGB == 0] = 1e-10

        minRGB = numpy.minimum.reduce([
            self.__chR, 
            self.__chG, 
            self.__chB
        ])
        saturation = 1 - (3 * (minRGB / sumRGB))
        saturation *= SATURATION_MAX

        return saturation

    def calculate_intensity(
        self
    ):
        sumRGB = (self.__chR + self.__chG + self.__chB)
        intensity = sumRGB / 3
        intensity *= INTENSITY_MAX

        return intensity

    def convert_rgb_to_hsi(
        self
    ):
        hue = self.calculate_hue()
        saturation = self.calculate_saturation()
        intensity = self.calculate_intensity()

        return (hue, saturation, intensity)
    
    def create_hsi_mask(
        self,
        minHue: "float" = 0, 
        maxHue: "float" = HUE_MAX,
        minSaturation: "float" = 0,
        maxSaturation: "float" = SATURATION_MAX,
        minIntensity: "float" = 0,
        maxIntensity: "float" = INTENSITY_MAX,
    ):
        h, s, i = self.convert_rgb_to_hsi()

        hueCheck1stCase = (h >= minHue) & (h <= maxHue)
        hueCheck2ndCase = (minHue > maxHue) & \
            (((h >= minHue) & (h <= 360)) | ((h >= 0) & (h <= maxHue)))
        hueCheck = hueCheck1stCase | hueCheck2ndCase

        saturationCheck = (s >= minSaturation) & (s <= maxSaturation)
        intensityCheck = (i >= minIntensity) & (i <= maxIntensity)

        mask = hueCheck & saturationCheck & intensityCheck

        return mask
