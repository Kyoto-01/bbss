from os import system
from tkinter import (
    ttk, 
    IntVar,
    filedialog,
    Misc
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
        master: "Misc",
        imagePath: "str"
    ):
        super().__init__(master)

        self.__imagePath: "str" = imagePath
        self.__image: "ImageTk" = None

        self.__lblImage: "ttk.Label" = None

        self.__create_lbl_image()

    def __create_lbl_image(
        self
    ):
        self.__lblImage = ttk.Label(self)
        self.__lblImage.pack()

    def update_image(
        self
    ):
        image = Image.open(self.__imagePath)
        base_width = 500
        wpercent = (base_width / float(image.size[0]))
        hsize = int((float(image.size[1]) * float(wpercent)))
        image = image.resize(
            size=(base_width, hsize), 
            resample=Image.Resampling.LANCZOS
        )
        self.__image = ImageTk.PhotoImage(image)
        self.__lblImage.configure(image=self.__image)

    def save_image(
        self,
        dst: "str"
    ):
        system(f"cp {self.__imagePath} {dst}")


class FrmImageFile(ttk.Frame):

    def __init__(
        self, 
        master: "Misc",
        imageView: "FrmImageView",
        imageScanner: "ImageScanner"
    ):
        super().__init__(master)

        self.__imageView: "FrmImageView" = imageView
        self.__imageScanner: "ImageScanner" = imageScanner

        self.__btnSelectImage: "ttk.Button" = None
        self.__btnSaveImage: "ttk.Button" = None

        self.__create_btn_select_image()
        self.__create_btn_save_image()

    def __create_btn_select_image(self):
        self.__btnSelectImage = ttk.Button(
            self,
            text="Select",
            command=self.__select_image
        )
        self.__btnSelectImage.pack(
            side="left"
        )

    def __create_btn_save_image(self):
        self.__btnSaveImage = ttk.Button(
            self,
            text="Save",
            command=self.__save_image
        )
        self.__btnSaveImage.pack(
            side="right"
        )

    def __select_image(self):
        inputImage = filedialog.askopenfilename(
            title="Select an image",
            initialdir="/"
        )
        self.__imageScanner.inputImagePath = inputImage
        self.__imageScanner.scan_image()
        self.__imageView.update_image()   

    def __save_image(self):
        dstDirectory = filedialog.askopenfilename(
            title="Save the image",
            initialdir="/"
        )
        self.__imageView.save_image(dstDirectory)


class FrmImageOptions(ttk.Frame):

    def __init__(
        self,
        master,
        imageView: "FrmImageView",
        imageScanner: "ImageScanner"
    ):
        super().__init__(master)

        self.__imageView: "FrmImageView" = imageView
        self.__imageScanner: "ImageScanner" = imageScanner

        self.__frmShadowOption: "FrmImageOption" = None
        self.__frmLightOption: "FrmImageOption" = None
        self.__frmLineOption: "FrmImageOption" = None

        self.__create_frm_shadow_option()
        self.__create_frm_light_option()
        self.__create_frm_line_option()

    def __create_frm_shadow_option(
        self
    ):
        self.__frmShadowOption = FrmImageOption(
            self,
            optionName="Shadow",
            imageView=self.__imageView,
            imageScanner=self.__imageScanner,
            hueMinCallback=self.__shadow_hue_min_callback,
            hueMaxCallback=self.__shadow_hue_max_callback,
            saturationMinCallback=self.__shadow_saturation_min_callback,
            saturationMaxCallback=self.__shadow_saturation_max_callback,
            intensityMinCallback=self.__shadow_intensity_min_callback,
            intensityMaxCallback=self.__shadow_intensity_max_callback
        )
        self.__frmShadowOption.pack()

    def __create_frm_light_option(
        self
    ):
        self.__frmLightOption = FrmImageOption(
            self,
            optionName="Light",
            imageView=self.__imageView,
            imageScanner=self.__imageScanner,
            hueMinCallback=self.__light_hue_min_callback,
            hueMaxCallback=self.__light_hue_max_callback,
            saturationMinCallback=self.__light_saturation_min_callback,
            saturationMaxCallback=self.__light_saturation_max_callback,
            intensityMinCallback=self.__light_intensity_min_callback,
            intensityMaxCallback=self.__light_intensity_max_callback
        )
        self.__frmLightOption.pack()

    def __create_frm_line_option(
        self
    ):
        self.__frmLineOption = FrmImageOption(
            self,
            optionName="Line",
            imageView=self.__imageView,
            imageScanner=self.__imageScanner,
            hueMinCallback=self.__line_hue_min_callback,
            hueMaxCallback=self.__line_hue_max_callback,
            saturationMinCallback=self.__line_saturation_min_callback,
            saturationMaxCallback=self.__line_saturation_max_callback,
            intensityMinCallback=self.__line_intensity_min_callback,
            intensityMaxCallback=self.__line_intensity_max_callback
        )
        self.__frmLineOption.pack()

    def __shadow_hue_min_callback(
        self
    ):
        self.__imageScanner.lastShadowHueMin = \
            self.__frmShadowOption.hueMin
        
    def __shadow_hue_max_callback(
        self
    ):
        self.__imageScanner.lastShadowHueMax = \
            self.__frmShadowOption.hueMax
        
    def __shadow_saturation_min_callback(
        self
    ):
        self.__imageScanner.lastShadowSaturationMin = \
            self.__frmShadowOption.saturationMin
        
    def __shadow_saturation_max_callback(
        self
    ):
        self.__imageScanner.lastShadowSaturationMax = \
            self.__frmShadowOption.saturationMax
        
    def __shadow_intensity_min_callback(
        self
    ):
        self.__imageScanner.lastShadowIntensityMin = \
            self.__frmShadowOption.intensityMin
        
    def __shadow_intensity_max_callback(
        self
    ):
        self.__imageScanner.lastShadowIntensityMax = \
            self.__frmShadowOption.intensityMax

    def __light_hue_min_callback(
        self
    ):
        self.__imageScanner.lastLightHueMin = \
            self.__frmLightOption.hueMin
        
    def __light_hue_max_callback(
        self
    ):
        self.__imageScanner.lastLightHueMax = \
            self.__frmLightOption.hueMax
        
    def __light_saturation_min_callback(
        self
    ):
        self.__imageScanner.lastLightSaturationMin = \
            self.__frmLightOption.saturationMin
        
    def __light_saturation_max_callback(
        self
    ):
        self.__imageScanner.lastLightSaturationMax = \
            self.__frmLightOption.saturationMax
        
    def __light_intensity_min_callback(
        self
    ):
        self.__imageScanner.lastLightIntensityMin = \
            self.__frmLightOption.intensityMin
        
    def __light_intensity_max_callback(
        self
    ):
        self.__imageScanner.lastLightIntensityMax = \
            self.__frmLightOption.intensityMax

    def __line_hue_min_callback(
        self
    ):
        self.__imageScanner.lastLineHueMin = \
            self.__frmLineOption.hueMin
        
    def __line_hue_max_callback(
        self
    ):
        self.__imageScanner.lastLineHueMax = \
            self.__frmLineOption.hueMax
        
    def __line_saturation_min_callback(
        self
    ):
        self.__imageScanner.lastLineSaturationMin = \
            self.__frmLineOption.saturationMin
        
    def __line_saturation_max_callback(
        self
    ):
        self.__imageScanner.lastLineSaturationMax = \
            self.__frmLineOption.saturationMax
        
    def __line_intensity_min_callback(
        self
    ):
        self.__imageScanner.lastLineIntensityMin = \
            self.__frmLineOption.intensityMin
        
    def __line_intensity_max_callback(
        self
    ):
        self.__imageScanner.lastLineIntensityMax = \
            self.__frmLineOption.intensityMax        


class FrmImageOption(ttk.Frame):

    def __init__(
        self,
        master: "Misc",
        optionName: "str",
        imageView: "FrmImageView",
        imageScanner: "ImageScanner",
        hueMinCallback: "function",
        hueMaxCallback: "function",
        saturationMinCallback: "function",
        saturationMaxCallback: "function",
        intensityMinCallback: "function",
        intensityMaxCallback: "function" 
    ):
        super().__init__(master)

        self.__imageView: "FrmImageView" = imageView
        self.__imageScanner: "ImageScanner" = imageScanner

        self.__lblOptionName: "ttk.Label" = None
        self.__frmHueMin: "FrmImageOptionProperty" = None
        self.__frmHueMax: "FrmImageOptionProperty" = None
        self.__frmSaturationMin: "FrmImageOptionProperty" = None
        self.__frmSaturationMax: "FrmImageOptionProperty" = None
        self.__frmIntensityMin: "FrmImageOptionProperty" = None
        self.__frmIntensityMax: "FrmImageOptionProperty" = None

        self.__create_option_name(optionName)
        self.__create_frm_hue_min(hueMinCallback)
        self.__create_frm_hue_max(hueMaxCallback)
        self.__create_frm_saturation_min(saturationMinCallback)
        self.__create_frm_saturation_max(saturationMaxCallback)
        self.__create_frm_intensity_min(intensityMinCallback)
        self.__create_frm_intensity_max(intensityMaxCallback)

    @property
    def hueMin(self):
        return self.__frmHueMin.value

    @property
    def hueMax(self):
        return self.__frmHueMax.value

    @property
    def saturationMin(self):
        return self.__frmSaturationMin.value

    @property
    def saturationMax(self):
        return self.__frmSaturationMax.value

    @property
    def intensityMin(self):
        return self.__frmIntensityMin.value

    @property
    def intensityMax(self):
        return self.__frmIntensityMax.value
        
    def __create_option_name(
        self,
        optionName: "str"
    ):
        self.__lblOptionName = ttk.Label(
            self,
            text=optionName
        )
        self.__lblOptionName.grid(
            column=0,
            row=0
        )

    def __create_frm_hue_min(
        self,
        callback: "function"
    ):
        self.__frmHueMin = FrmImageOptionProperty(
         self,
            name="Hue min.:",
            minValue=0,
            maxValue=HUE_MAX,
            callback=callback,
            imageView=self.__imageView,
            imageScanner=self.__imageScanner
        )
        self.__frmHueMin.grid(
            column=0,
            row=1
        )

    def __create_frm_hue_max(
        self,
        callback: "function"
    ):
        self.__frmHueMax = FrmImageOptionProperty(
            self,
            name="Hue max.:",
            minValue=0,
            maxValue=HUE_MAX,
            callback=callback,
            imageView=self.__imageView,
            imageScanner=self.__imageScanner
        )
        self.__frmHueMax.grid(
            column=0,
            row=2
        )

    def __create_frm_saturation_min(
        self,
        callback: "function"
    ):
        self.__frmSaturationMin = FrmImageOptionProperty(
            self,
            name="Sat. min.:",
            minValue=0,
            maxValue=SATURATION_MAX,
            callback=callback,
            imageView=self.__imageView,
            imageScanner=self.__imageScanner
        )
        self.__frmSaturationMin.grid(
            column=1,
            row=1
        )

    def __create_frm_saturation_max(
        self,
        callback: "function"
    ):
        self.__frmSaturationMax = FrmImageOptionProperty(
            self,
            name="Sat. max.:",
            minValue=0,
            maxValue=SATURATION_MAX,
            callback=callback,
            imageView=self.__imageView,
            imageScanner=self.__imageScanner
        )
        self.__frmSaturationMax.grid(
            column=1,
            row=2
        )

    def __create_frm_intensity_min(
        self,
        callback: "function"
    ):
        self.__frmIntensityMin = FrmImageOptionProperty(
            self,
            name="Int. min.:",
            minValue=0,
            maxValue=INTENSITY_MAX,
            callback=callback,
            imageView=self.__imageView,
            imageScanner=self.__imageScanner
        )
        self.__frmIntensityMin.grid(
            column=2,
            row=1
        )

    def __create_frm_intensity_max(
        self,
        callback: "function"
    ):
        self.__frmIntensityMax = FrmImageOptionProperty(
            self,
            name="Int. max.:",
            minValue=0,
            maxValue=INTENSITY_MAX,
            callback=callback,
            imageView=self.__imageView,
            imageScanner=self.__imageScanner
        )
        self.__frmIntensityMax.grid(
            column=2,
            row=2
        )


class FrmImageOptionProperty(ttk.Frame):

    def __init__(
        self,
        master: "Misc",
        name: "str",
        minValue: "int",
        maxValue: "int",
        callback: "function",
        imageView: "FrmImageView",
        imageScanner: "ImageScanner"   
    ):
        super().__init__(master)

        self.__callback = callback
        self.__imageView: "FrmImageView" = imageView
        self.__imageScanner: "ImageScanner" = imageScanner

        self.__lblPropertyName: "ttk.Label" = None
        self.__varPropertyValue: "IntVar" = None
        self.__spbPropertyField: "ttk.Spinbox" = None

        self.__create_lbl_property_name(name)
        self.__create_var_property_value()
        self.__create_sbp_property_field(minValue, maxValue)

    @property
    def value(self):
        return self.__varPropertyValue.get()

    def __create_lbl_property_name(
        self,
        propertyName: "str"
    ):
        self.__lblPropertyName = ttk.Label(
            self,
            text=propertyName
        )
        self.__lblPropertyName.pack(
            side="left"
        )

    def __create_sbp_property_field(
        self,
        minValue: "int",
        maxValue: "int",
    ):
        self.__spbPropertyField = ttk.Spinbox(
            self, 
            from_=minValue,
            to=maxValue,
            textvariable=self.__varPropertyValue,
            command=self.__base_callback
        )
        self.__spbPropertyField.pack(
            side="right"
        )

    def __create_var_property_value(
        self
    ):
        self.__varPropertyValue = IntVar(self)

    def __base_callback(
        self
    ):
        self.__callback()
        self.__imageScanner.scan_image()
        self.__imageView.update_image()


class FrmApp(ttk.Frame):

    def __init__(
        self, 
        master,
        otputImagePath: "str",
        title: "str" = "App",
        maxWidth: "int" = 0,
        maxHeight: "int" = 0,
        minWidth: "int" = 0,
        minHeight: "int" = 0
    ):
        super().__init__(master)
    
        self.__outputImagePath: "str" = otputImagePath
        self.__imageScanner: "ImageScanner" = None

        self.__frmImageView: "FrmImageView" = None
        self.__frmImageFile: "FrmImageFile" = None
        self.__frmImageOptions: "FrmImageOptions" = None

        self.__setup(
            title, 
            maxWidth, 
            maxHeight, 
            minWidth, 
            minHeight
        )

        self.__create_frm_image_view()
        self.__create_frm_image_file()
        self.__create_frm_image_options()

    def __setup(
        self,
        title: "str",
        maxWidth: "int",
        maxHeight: "int",
        minWidth: "int",
        minHeight: "int"
    ):
        self.master.title(title)
        self.master.maxsize(maxWidth, maxHeight)
        self.master.minsize(minWidth, minHeight)
        self.__imageScanner = ImageScanner(self.__outputImagePath)
        self.pack()

    def __create_frm_image_view(
        self
    ):
        self.__frmImageView = FrmImageView(
            self,
            imagePath=self.__outputImagePath
        )
        self.__frmImageView.pack(
            side="left"
        )

    def __create_frm_image_file(
        self
    ):
        self.__frmImageFile = FrmImageFile(
            self,
            imageView=self.__frmImageView,
            imageScanner=self.__imageScanner
        )
        self.__frmImageFile.pack()

    def __create_frm_image_options(
        self
    ):
        self.__frmImageOptions = FrmImageOptions(
            self,
            imageView=self.__frmImageView,
            imageScanner=self.__imageScanner
        )
        self.__frmImageOptions.pack()


system("cp output.bmp output_copy.bmp")

FrmApp = FrmApp(
    master=None,
    otputImagePath="output.bmp",
    title="Sakuga Scan",
    minWidth=0,
    minHeight=0,
    maxWidth=0,
    maxHeight=0
)

FrmApp.mainloop()

system("cp output_copy.bmp output.bmp")
system("rm output_copy.bmp")
