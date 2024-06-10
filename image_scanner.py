import numpy
import cv2

from hsi import (
    HSI,
    HUE_MAX,
    SATURATION_MAX,
    INTENSITY_MAX
)


class ImageScannerEntity:
    
    def __init__(
        self,
        hsiFilter: "HSI" = None
    ):
        self.__hsiFilter: "HSI" = hsiFilter
        self.__lastHueMin: "int" = 0
        self.__lastHueMax: "int" = HUE_MAX
        self.__lastSaturationMin: "int" = 0
        self.__lastSaturationMax: "int" = SATURATION_MAX
        self.__lastIntensityMin: "int" = 0
        self.__lastIntensityMax: "int" = INTENSITY_MAX
        self.__lastScan: "cv2.Mat" = None

    @property
    def lastHueMin(self):
        return self.__lastHueMin

    @lastHueMin.setter
    def lastHueMin(self, value):
        self.__lastHueMin = value

    @property
    def lastHueMax(self):
        return self.__lastHueMax

    @lastHueMax.setter
    def lastHueMax(self, value):
        self.__lastHueMax = value

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

    @property
    def lastScan(self):
        return self.__lastScan
    
    def set_hsi_filter(
        self,
        hsiFilter: "HSI"
    ):
        self.__hsiFilter = hsiFilter

    def scan_image(
        self
    ):
        assert self.__hsiFilter is not None, "Missing HSI filter."

        self.__lastScan = self.__hsiFilter.create_hsi_mask(
            minHue=self.__lastHueMin,
            maxHue=self.__lastHueMax,
            minSaturation=self.__lastSaturationMin,
            maxSaturation=self.__lastSaturationMax,
            minIntensity=self.__lastIntensityMin,
            maxIntensity=self.__lastIntensityMax
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
        self.__shadowScanner: "ImageScannerEntity" = None
        self.__lightScanner: "ImageScannerEntity" = None
        self.__lineScanner: "ImageScannerEntity" = None

        self.__setup()

    @property
    def inputImagePath(self):
        return self.__inputImagePath

    @inputImagePath.setter
    def inputImagePath(self, value):
        self.__inputImagePath = value
        self.__put_image()

    @property
    def outputImagePath(self):
        return self.__outputImagePath

    @property
    def shadowScanner(self):
        return self.__shadowScanner
    
    @property
    def lightScanner(self):
        return self.__lightScanner
    
    @property
    def lineScanner(self):
        return self.__lineScanner

    def __setup(
        self
    ):
        self.__shadowScanner = ImageScannerEntity()
        self.__lightScanner = ImageScannerEntity()
        self.__lineScanner = ImageScannerEntity()
        self.__put_image()

    def __put_image(
        self
    ):
        if self.__inputImagePath:
            self.__imageRGB = cv2.imread(self.__inputImagePath)
            self.__imageRGB = self.__imageRGB[:, :, [2, 1, 0]]
            self.__hsiFilter = HSI(self.__imageRGB)
            self.__shadowScanner.set_hsi_filter(self.__hsiFilter)
            self.__lightScanner.set_hsi_filter(self.__hsiFilter)
            self.__lineScanner.set_hsi_filter(self.__hsiFilter)
    
    def scan_image(
        self
    ):
        self.__shadowScanner.scan_image()
        self.__lightScanner.scan_image()
        self.__lineScanner.scan_image()

        shadowColor = [0, 0, 255] # red in BGR
        lightColor = [255, 0, 0] # blue in BGR
        lineColor = [0, 0, 0] # black in BGR

        scannedImage = numpy.ones(self.__imageRGB.shape) * 255
        scannedImage[self.__lineScanner.lastScan == 1] = lineColor
        scannedImage[self.__lightScanner.lastScan == 1] = lightColor
        scannedImage[self.__shadowScanner.lastScan == 1] = shadowColor

        cv2.imwrite(self.__outputImagePath, scannedImage)
