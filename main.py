import numpy
import cv2

from tkinter import ttk
from PIL import (
    ImageTk,
    Image
)

from hsi import (
    HSI,
    HUE_MAX,
    SATURATION_MAX,
    INTENSITY_MAX
)

imgRGB = cv2.imread("elfo_soldado_150dpi_adjusted.jpg")
imgRGB = imgRGB[:, :, [2, 1, 0]]
imgRGB = cv2.resize(
    imgRGB, 
    dsize=(619, 877)
)

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

class AppUI(ttk.Frame):

    def __init__(
        self, 
        master=None,
        title: "str" = "App",
        maxWidth: "int" = 0,
        maxHeight: "int" = 0,
        minWidth: "int" = 0,
        minHeight: "int" = 0
    ):
        super().__init__(master)
        self.__setup(
            title, 
            maxWidth, 
            maxHeight, 
            minWidth, 
            minHeight
        )

        # left frame - Image view

        self.__frmImage: "ttk.Frame" = None
        self.__lblImage: "ttk.Label" = None
        self.__image: "ImageTk" = None

        # right frame - Options

        self.__frmOptions: "ttk.Frame" = None

        self.__frmHueShadow: "ttk.Frame" = None
        self.__lblHueShadow: "ttk.Label" = None
        self.__spbHueShadowMin: "ttk.Spinbox" = None
        self.__spbHueShadowMax: "ttk.Spinbox" = None

        self.__frmHueLight: "ttk.Frame" = None
        self.__lblHueLight: "ttk.Label" = None
        self.__spbHueLightMin: "ttk.Spinbox" = None
        self.__spbHueLightMax: "ttk.Spinbox" = None

        self.__frmSaturation: "ttk.Frame" = None
        self.__lblSaturation: "ttk.Label" = None
        self.__spbSaturationMin: "ttk.Spinbox" = None
        self.__spbSaturationMax: "ttk.Spinbox" = None

        self.__frmIntensity: "ttk.Frame" = None
        self.__lblIntensity: "ttk.Label" = None
        self.__spbIntensityMin: "ttk.Spinbox" = None
        self.__spbIntensityMax: "ttk.Spinbox" = None

        self.__build()

    def __setup(
        self,
        title: "str" = "App",
        maxWidth: "int" = 0,
        maxHeight: "int" = 0,
        minWidth: "int" = 0,
        minHeight: "int" = 0
    ):
        self.master.title(title)
        self.master.maxsize(maxWidth, maxHeight)
        self.master.minsize(minWidth, minHeight)

    def __create_frm_image(
        self
    ):
        # image view root frame
        self.__frmImage = ttk.Frame(self)
        self.__frmImage.grid(column=0, row=0)

        # image view image
        self.__lblImage = ttk.Label(self.__frmImage)
        self.__lblImage.pack()

    def __create_frm_options(
        self
    ):
        # options root frame
        self.__frmOptions = ttk.Frame(self)
        self.__frmOptions.grid(column=1, row=0)

    def __build(
        self
    ):
        self.pack()
        self.__create_frm_image()
        self.__create_frm_options()

    def update_image_view(
        self, 
        imagePath: "str"
    ):
        self.__image = Image.open(imagePath)
        self.__image = ImageTk.PhotoImage(self.__image)
        self.__lblImage.configure(image=self.__image)


app = AppUI(
    title="Sakuga Scan",
    minWidth=0,
    minHeight=0,
    maxWidth=0,
    maxHeight=0
)

app.update_image_view("hsi.bmp")

app.mainloop()
