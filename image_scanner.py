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
        
        self.__lastHueShadowMin: "int" = 0
        self.__lastHueShadowMax: "int" = HUE_MAX
        self.__lastHueLightMin: "int" = 0
        self.__lastHueLightMax: "int" = HUE_MAX
        self.__lastSaturationMin: "int" = 0
        self.__lastSaturationMax: "int" = SATURATION_MAX
        self.__lastIntensityMin: "int" = 0
        self.__lastIntensityMax: "int" = INTENSITY_MAX

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
    def lastHueShadowMin(self):
        return self.__lastHueShadowMin

    @lastHueShadowMin.setter
    def lastHueShadowMin(self, value):
        self.__lastHueShadowMin = value

    @property
    def lastHueShadowMax(self):
        return self.__lastHueShadowMax

    @lastHueShadowMax.setter
    def lastHueShadowMax(self, value):
        self.__lastHueShadowMax = value

    @property
    def lastHueLightMin(self):
        return self.__lastHueLightMin

    @lastHueLightMin.setter
    def lastHueLightMin(self, value):
        self.__lastHueLightMin = value

    @property
    def lastHueLightMax(self):
        return self.__lastHueLightMax

    @lastHueLightMax.setter
    def lastHueLightMax(self, value):
        self.__lastHueLightMax = value

    @property
    def lastSaturationMin(self):
        return self.__lastSaturationMin

    @lastSaturationMin.setter
    def lastSaturationMin(self, value):
        self.__lastSaturationMin = value

    @property
    def lastSaturationMax(self):
        return self.__lastSaturationMax

    @lastSaturationMax.setter
    def lastSaturationMax(self, value):
        self.__lastSaturationMax = value

    @property
    def lastIntensityMin(self):
        return self.__lastIntensityMin

    @lastIntensityMin.setter
    def lastIntensityMin(self, value):
        self.__lastIntensityMin = value

    @property
    def lastIntensityMax(self):
        return self.__lastIntensityMax

    @lastIntensityMax.setter
    def lastIntensityMax(self, value):
        self.__lastIntensityMax = value

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
            minHue=self.__lastHueShadowMin,
            maxHue=self.__lastHueShadowMax,
            minIntensity=self.__lastIntensityMin,
            maxIntensity=self.__lastIntensityMax,
            minSaturation=self.__lastSaturationMin,
            maxSaturation=self.__lastSaturationMax
        )

        lightMask = self.__hsiFilter.create_hsi_mask(
            minHue=self.__lastHueLightMin,
            maxHue=self.__lastHueLightMax,
            minIntensity=self.__lastIntensityMin,
            maxIntensity=self.__lastIntensityMax,
            minSaturation=self.__lastSaturationMin,
            maxSaturation=self.__lastSaturationMax
        )

        lineMask = self.__hsiFilter.create_hsi_mask(
            minIntensity=self.__lastIntensityMin,
            maxIntensity=self.__lastIntensityMax,
            minSaturation=self.__lastSaturationMin,
            maxSaturation=self.__lastSaturationMax
        )

        scannedImage = numpy.ones(self.__imageRGB.shape) * 255
        scannedImage[shadowMask == 1] = [0, 0, 255]
        scannedImage[lightMask == 1] = [255, 0, 0]
        scannedImage[lineMask == 1] = [0, 0, 0]

        cv2.imwrite(self.__outputImagePath, scannedImage)
