from os import system

from tkinter import (
    ttk, 
    IntVar,
    filedialog
)

from PIL import (
    ImageTk,
    Image
)

from image_scanner import ImageScanner
from hsi import (
    HUE_MAX,
    SATURATION_MAX,
    INTENSITY_MAX
)


class FrmImageView(ttk.Frame):
    
    def __init__(
        self,
        imagePath: "str"
    ):
        self.__imagePath: "str" = imagePath
        self.__image: "ImageTk" = None
        self.__lblImage: "ttk.Label" = None


class FrmImageSelection(ttk.Frame):

    def __init__(
        self
    ):
        self.__btnSelectImage: "ttk.Button" = None


class FrmImageConfigProperty(ttk.Frame):

    def __init__(
        self
    ):
        self.__lblPropertyName: "ttk.Spinbox" = None
        self.__spbPropertyField: "ttk.Spinbox" = None
        self.__varPropertyValue: "IntVar" = None


class FrmImageConfig(ttk.Frame):

    def __init__(
        self
    ):
        self.__lblConfigName: "ttk.Label" = None
        self.__frmHueMin: "FrmImageConfigProperty" = None
        self.__frmHueMax: "FrmImageConfigProperty" = None
        self.__frmSaturationMin: "FrmImageConfigProperty" = None
        self.__frmSaturationMax: "FrmImageConfigProperty" = None
        self.__frmIntensityMin: "FrmImageConfigProperty" = None
        self.__frmIntensityMax: "FrmImageConfigProperty" = None


class FrmOptions(ttk.Frame):

    def __init__(
        self
    ):
        self.__frmImageShadowConfig: "FrmImageConfig" = None
        self.__frmImageLightConfig: "FrmImageConfig" = None
        self.__frmImageLineConfig: "FrmImageConfig" = None


class FrmApp(ttk.Frame):

    def __init__(
        self, 
        imagePath: "str",
        master=None,
        title: "str" = "App",
        maxWidth: "int" = 0,
        maxHeight: "int" = 0,
        minWidth: "int" = 0,
        minHeight: "int" = 0
    ):
        super().__init__(master)
        
        self.__scanner: "ImageScanner" = None
        self.__frmImageView: "FrmImageView" = None
        self.__frmOptions: "FrmOptions" = None

        self.__setup(
            title, 
            maxWidth, 
            maxHeight, 
            minWidth, 
            minHeight
        )
        self.__build()

    def __setup(
        self,
        title: "str" = "FrmApp",
        maxWidth: "int" = 0,
        maxHeight: "int" = 0,
        minWidth: "int" = 0,
        minHeight: "int" = 0
    ):
        self.master.title(title)
        self.master.maxsize(maxWidth, maxHeight)
        self.master.minsize(minWidth, minHeight)

        self.__scanner = ImageScanner(
            outputImagePath=self.__imagePath
        )

    def __build(
        self
    ):
        self.pack()
        self.__create_frm_image(self)
        self.__create_frm_options(self)

    def __create_frm_image(
        self,
        master
    ):
        self.__frmImage = ttk.Frame(master)
        self.__frmImage.grid(column=0, row=0)
        self.__create_lbl_image(self.__frmImage)
        self.__update_image_view()

    def __create_lbl_image(
        self,
        master
    ):
        self.__lblImage = ttk.Label(master)
        self.__lblImage.pack()

    def __update_image_view(
        self
    ):
        image = Image.open(self.__imagePath)
        base_width = 500
        wpercent = (base_width / float(image.size[0]))
        hsize = int((float(image.size[1]) * float(wpercent)))
        image = image.resize((base_width, hsize), Image.Resampling.LANCZOS)

        self.__image = image
        self.__image = ImageTk.PhotoImage(self.__image)
        self.__lblImage.configure(image=self.__image)

    def __create_frm_options(
        self,
        master
    ):
        self.__frmOptions = ttk.Frame(master)
        self.__frmOptions.grid(column=1, row=0)
        self.__create_frm_select_image(self.__frmOptions)
        self.__create_frm_hue_shadow(self.__frmOptions)
        self.__create_frm_hue_light(self.__frmOptions)
        self.__create_frm_saturation(self.__frmOptions)
        self.__create_frm_intensity(self.__frmOptions)

    def __create_frm_select_image(
        self, 
        master
    ):
        self.__frmSelectImage = ttk.Frame(master)
        self.__frmSelectImage.pack()
        self.__create_btn_select_image(self.__frmSelectImage)

    def __create_btn_select_image(
        self,
        master
    ):
        self.__btnSelectImage = ttk.Button(
            master,
            text="Select an image",
            command=self.__select_image
        )
        self.__btnSelectImage.pack()

    def __select_image(self):
        inputImage = filedialog.askopenfilename(
            title="Select an image",
            initialdir="/"
        )
        self.__scanner.inputImagePath = inputImage
        self.__scanner.scan_image()
        self.__update_image_view()

    def __create_frm_hue_shadow(
        self, 
        master
    ):
        self.__frmHueShadow = ttk.Frame(master)
        self.__frmHueShadow.pack()
        self.create_lbl_hue_shadow(self.__frmHueShadow)
        self.create_spb_hue_shadow_min(self.__frmHueShadow)
        self.create_spb_hue_shadow_max(self.__frmHueShadow)

    def create_lbl_hue_shadow(
        self,
        master
    ):
        self.__lblHueShadow = ttk.Label(
            master, 
            text="Hue Shadow"
        )
        self.__lblHueShadow.pack()

    def create_spb_hue_shadow_min(
        self,
        master
    ):
        self.__varHueShadowMin = IntVar(value=0)
        self.__spbHueShadowMin = ttk.Spinbox(
            master, 
            from_=0,
            to=HUE_MAX,
            textvariable=self.__varHueShadowMin,
            command=self.update_spb_hue_shadow_min
        )
        self.__spbHueShadowMin.pack()

    def update_spb_hue_shadow_min(
        self
    ):
        self.__scanner.lastHueShadowMin = self.__varHueShadowMin.get()
        self.__scanner.scan_image()
        self.__update_image_view()

    def create_spb_hue_shadow_max(
        self,
        master
    ):
        self.__varHueShadowMax = IntVar(value=0)
        self.__spbHueShadowMax = ttk.Spinbox(
            master, 
            from_=0,
            to=HUE_MAX,
            textvariable=self.__varHueShadowMax,
            command=self.update_spb_hue_shadow_max
        )
        self.__spbHueShadowMax.pack()

    def update_spb_hue_shadow_max(
        self
    ):
        self.__scanner.lastHueShadowMax = self.__varHueShadowMax.get()
        self.__scanner.scan_image()
        self.__update_image_view()

    def __create_frm_hue_light(
        self, 
        master
    ):
        self.__frmHueLight = ttk.Frame(master)
        self.__frmHueLight.pack()
        self.create_lbl_hue_light(self.__frmHueLight)
        self.create_spb_hue_light_min(self.__frmHueLight)
        self.create_spb_hue_light_max(self.__frmHueLight)

    def create_lbl_hue_light(
        self,
        master
    ):
        self.__lblHueLight = ttk.Label(
            master, 
            text="Hue Light"
        )
        self.__lblHueLight.pack()

    def create_spb_hue_light_min(
        self,
        master
    ):
        self.__varHueLightMin = IntVar(value=0)
        self.__spbHueLightMin = ttk.Spinbox(
            master, 
            from_=0,
            to=HUE_MAX,
            textvariable=self.__varHueLightMin,
            command=self.update_spb_hue_light_min
        )
        self.__spbHueLightMin.pack()

    def update_spb_hue_light_min(
        self
    ):
        self.__scanner.lastHueLightMin = self.__varHueLightMin.get()
        self.__scanner.scan_image()
        self.__update_image_view()

    def create_spb_hue_light_max(
        self,
        master
    ):
        self.__varHueLightMax = IntVar(value=0)
        self.__spbHueLightMax = ttk.Spinbox(
            master, 
            from_=0,
            to=HUE_MAX,
            textvariable=self.__varHueLightMax,
            command=self.update_spb_hue_light_max
        )
        self.__spbHueLightMax.pack()

    def update_spb_hue_light_max(
        self
    ):
        self.__scanner.lastHueLightMax = self.__varHueLightMax.get()
        self.__scanner.scan_image()
        self.__update_image_view()

    def __create_frm_saturation(
        self, 
        master
    ):
        self.__frmSaturation = ttk.Frame(master)
        self.__frmSaturation.pack()
        self.create_lbl_saturation(self.__frmSaturation)
        self.create_spb_saturation_min(self.__frmSaturation)
        self.create_spb_saturation_max(self.__frmSaturation)

    def create_lbl_saturation(
        self,
        master
    ):
        self.__lblSaturation = ttk.Label(
            master, 
            text="Hue Saturation"
        )
        self.__lblSaturation.pack()

    def create_spb_saturation_min(
        self,
        master
    ):
        self.__varSaturationMin = IntVar(value=0)
        self.__spbSaturationMin = ttk.Spinbox(
            master, 
            from_=0,
            to=SATURATION_MAX,
            textvariable=self.__varSaturationMin,
            command=self.update_spb_saturation_min
        )
        self.__spbSaturationMin.pack()

    def update_spb_saturation_min(
        self
    ):
        self.__scanner.lastSaturationMin = self.__varSaturationMin.get()
        self.__scanner.scan_image()
        self.__update_image_view()

    def create_spb_saturation_max(
        self,
        master
    ):
        self.__varSaturationMax = IntVar(value=0)
        self.__spbSaturationMax = ttk.Spinbox(
            master, 
            from_=0,
            to=SATURATION_MAX,
            textvariable=self.__varSaturationMax,
            command=self.update_spb_saturation_max
        )
        self.__spbSaturationMax.pack()

    def update_spb_saturation_max(
        self
    ):
        self.__scanner.lastSaturationMax = self.__varSaturationMax.get()
        self.__scanner.scan_image()
        self.__update_image_view()

    def __create_frm_intensity(
        self, 
        master
    ):
        self.__frmIntensity = ttk.Frame(master)
        self.__frmIntensity.pack()
        self.create_lbl_intensity(self.__frmIntensity)
        self.create_spb_intensity_min(self.__frmIntensity)
        self.create_spb_intensity_max(self.__frmIntensity)

    def create_lbl_intensity(
        self,
        master
    ):
        self.__lblIntensity = ttk.Label(
            master, 
            text="Hue Intensity"
        )
        self.__lblIntensity.pack()

    def create_spb_intensity_min(
        self,
        master
    ):
        self.__varIntensityMin = IntVar(value=0)
        self.__spbIntensityMin = ttk.Spinbox(
            master, 
            from_=0,
            to=INTENSITY_MAX,
            textvariable=self.__varIntensityMin,
            command=self.update_spb_intensity_min
        )
        self.__spbIntensityMin.pack()

    def update_spb_intensity_min(
        self
    ):
        self.__scanner.lastIntensityMin = self.__varIntensityMin.get()
        self.__scanner.scan_image()
        self.__update_image_view()

    def create_spb_intensity_max(
        self,
        master
    ):
        self.__varIntensityMax = IntVar(value=0)
        self.__spbIntensityMax = ttk.Spinbox(
            master, 
            from_=0,
            to=INTENSITY_MAX,
            textvariable=self.__varIntensityMax,
            command=self.update_spb_intensity_max
        )
        self.__spbIntensityMax.pack()
    
    def update_spb_intensity_max(
        self
    ):
        self.__scanner.lastIntensityMax = self.__varIntensityMax.get()
        self.__scanner.scan_image()
        self.__update_image_view()


system("cp output.bmp output_copy.bmp")

FrmApp = FrmApp(
    imagePath="output.bmp",
    title="Sakuga Scan",
    minWidth=0,
    minHeight=0,
    maxWidth=0,
    maxHeight=0
)

FrmApp.mainloop()

system("cp output_copy.bmp output.bmp")
system("rm output_copy.bmp")
