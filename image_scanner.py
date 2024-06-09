import numpy
import cv2

from hsi import (
    HSI,
    HUE_MAX,
    SATURATION_MAX,
    INTENSITY_MAX
)


class ImageScanner:

    def __init__(
        self,
        outputImagePath: "str",
        inputImagePath: "str" = None
    ):
        self.__inputImagePath: "str" = inputImagePath
        self.__outputImagePath: "str" = outputImagePath
        self.__imageRGB: "cv2.Mat" = None
        self.__hsiFilter: "HSI" = None
        
        self.__lastShadowHueMin: "int" = 0
        self.__lastShadowHueMax: "int" = HUE_MAX
        self.__lastShadowSaturationMin: "int" = 0
        self.__lastShadowSaturationMax: "int" = SATURATION_MAX
        self.__lastShadowIntensityMin: "int" = 0
        self.__lastShadowIntensityMax: "int" = INTENSITY_MAX

        self.__lastLightHueMin: "int" = 0
        self.__lastLightHueMax: "int" = HUE_MAX
        self.__lastLightSaturationMin: "int" = 0
        self.__lastLightSaturationMax: "int" = SATURATION_MAX
        self.__lastLightIntensityMin: "int" = 0
        self.__lastLightIntensityMax: "int" = INTENSITY_MAX

        self.__lastLineHueMin: "int" = 0
        self.__lastLineHueMax: "int" = HUE_MAX
        self.__lastLineSaturationMin: "int" = 0
        self.__lastLineSaturationMax: "int" = SATURATION_MAX
        self.__lastLineIntensityMin: "int" = 0
        self.__lastLineIntensityMax: "int" = INTENSITY_MAX

        self.__setup()

    @property
    def inputImagePath(self):
        return self.__inputImagePath

    @inputImagePath.setter
    def inputImagePath(self, value):
        self.__inputImagePath = value
        self.__setup()

    @property
    def outputImagePath(self):
        return self.__outputImagePath

    @property
    def lastShadowHueMin(self):
        return self.__lastShadowHueMin

    @lastShadowHueMin.setter
    def lastShadowHueMin(self, value):
        self.__lastShadowHueMin = value

    @property
    def lastShadowHueMax(self):
        return self.__lastShadowHueMax

    @lastShadowHueMax.setter
    def lastShadowHueMax(self, value):
        self.__lastShadowHueMax = value

    @property
    def lastShadowSaturationMin(self):
        return self.__lastShadowSaturationMin

    @lastShadowSaturationMin.setter
    def lastShadowSaturationMin(self, value):
        self.__lastShadowSaturationMin = value

    @property
    def lastShadowSaturationMax(self):
        return self.__lastShadowSaturationMax

    @lastShadowSaturationMax.setter
    def lastShadowSaturationMax(self, value):
        self.__lastShadowSaturationMax = value

    @property
    def lastShadowIntensityMin(self):
        return self.__lastShadowIntensityMin

    @lastShadowIntensityMin.setter
    def lastShadowIntensityMin(self, value):
        self.__lastShadowIntensityMin = value

    @property
    def lastShadowIntensityMax(self):
        return self.__lastShadowIntensityMax

    @lastShadowIntensityMax.setter
    def lastShadowIntensityMax(self, value):
        self.__lastShadowIntensityMax = value

    @property
    def lastLightHueMin(self):
        return self.__lastLightHueMin

    @lastLightHueMin.setter
    def lastLightHueMin(self, value):
        self.__lastLightHueMin = value

    @property
    def lastLightHueMax(self):
        return self.__lastLightHueMax

    @lastLightHueMax.setter
    def lastLightHueMax(self, value):
        self.__lastLightHueMax = value

    @property
    def lastLightSaturationMin(self):
        return self.__lastLightSaturationMin

    @lastLightSaturationMin.setter
    def lastLightSaturationMin(self, value):
        self.__lastLightSaturationMin = value

    @property
    def lastLightSaturationMax(self):
        return self.__lastLightSaturationMax

    @lastLightSaturationMax.setter
    def lastLightSaturationMax(self, value):
        self.__lastLightSaturationMax = value

    @property
    def lastLightIntensityMin(self):
        return self.__lastLightIntensityMin

    @lastLightIntensityMin.setter
    def lastLightIntensityMin(self, value):
        self.__lastLightIntensityMin = value

    @property
    def lastLightIntensityMax(self):
        return self.__lastLightIntensityMax

    @lastLightIntensityMax.setter
    def lastLightIntensityMax(self, value):
        self.__lastLightIntensityMax = value

    @property
    def lastLineHueMin(self):
        return self.__lastLineHueMin

    @lastLineHueMin.setter
    def lastLineHueMin(self, value):
        self.__lastLineHueMin = value

    @property
    def lastLineHueMax(self):
        return self.__lastLineHueMax

    @lastLineHueMax.setter
    def lastLineHueMax(self, value):
        self.__lastLineHueMax = value

    @property
    def lastLineSaturationMin(self):
        return self.__lastLineSaturationMin

    @lastLineSaturationMin.setter
    def lastLineSaturationMin(self, value):
        self.__lastLineSaturationMin = value

    @property
    def lastLineSaturationMax(self):
        return self.__lastLineSaturationMax

    @lastLineSaturationMax.setter
    def lastLineSaturationMax(self, value):
        self.__lastLineSaturationMax = value

    @property
    def lastLineIntensityMin(self):
        return self.__lastLineIntensityMin

    @lastLineIntensityMin.setter
    def lastLineIntensityMin(self, value):
        self.__lastLineIntensityMin = value

    @property
    def lastLineIntensityMax(self):
        return self.__lastLineIntensityMax

    @lastLineIntensityMax.setter
    def lastLineIntensityMax(self, value):
        self.__lastLineIntensityMax = value

    def __setup(
        self
    ):
        if self.__inputImagePath:
            self.__imageRGB = cv2.imread(self.__inputImagePath)
            self.__imageRGB = self.__imageRGB[:, :, [2, 1, 0]]
            self.__hsiFilter = HSI(self.__imageRGB)
    
    def scan_image(
        self
    ):
        shadowMask = self.__hsiFilter.create_hsi_mask(
            minHue=self.__lastShadowHueMin,
            maxHue=self.__lastShadowHueMax,
            minSaturation=self.__lastShadowSaturationMin,
            maxSaturation=self.__lastShadowSaturationMax,
            minIntensity=self.__lastShadowIntensityMin,
            maxIntensity=self.__lastShadowIntensityMax
        )

        lightMask = self.__hsiFilter.create_hsi_mask(
            minHue=self.__lastLightHueMin,
            maxHue=self.__lastLightHueMax,
            minSaturation=self.__lastLightSaturationMin,
            maxSaturation=self.__lastLightSaturationMax,
            minIntensity=self.__lastLightIntensityMin,
            maxIntensity=self.__lastLightIntensityMax
        )

        lineMask = self.__hsiFilter.create_hsi_mask(
            minHue=self.__lastLineHueMin,
            maxHue=self.__lastLineHueMax,
            minSaturation=self.__lastLineSaturationMin,
            maxSaturation=self.__lastLineSaturationMax,
            minIntensity=self.__lastLineIntensityMin,
            maxIntensity=self.__lastLineIntensityMax
        )

        scannedImage = numpy.ones(self.__imageRGB.shape) * 255
        scannedImage[lineMask == 1] = [0, 0, 0]
        scannedImage[shadowMask == 1] = [0, 0, 255]
        scannedImage[lightMask == 1] = [255, 0, 0]

        cv2.imwrite(self.__outputImagePath, scannedImage)
