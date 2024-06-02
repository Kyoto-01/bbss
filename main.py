from os import system

from tkinter import (
    ttk, 
    filedialog
)

from PIL import (
    ImageTk,
    Image
)

from image_scanner import ImageScanner


class App(ttk.Frame):

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

        # left frame - image view
        self.__imagePath: "str" = imagePath
        self.__image: "ImageTk" = None
        self.__frmImage: "ttk.Frame" = None
        self.__lblImage: "ttk.Label" = None

        # right frame - options
        self.__frmOptions: "ttk.Frame" = None

        # right frame - options - hue shadow
        self.__frmSelectImage: "ttk.Frame" = None
        self.__btnSelectImage: "ttk.Button" = None

        # right frame - options - hue shadow
        self.__frmHueShadow: "ttk.Frame" = None
        self.__lblHueShadow: "ttk.Label" = None
        self.__spbHueShadowMin: "ttk.Spinbox" = None
        self.__spbHueShadowMax: "ttk.Spinbox" = None

        # right frame - options - hue light
        self.__frmHueLight: "ttk.Frame" = None
        self.__lblHueLight: "ttk.Label" = None
        self.__spbHueLightMin: "ttk.Spinbox" = None
        self.__spbHueLightMax: "ttk.Spinbox" = None

        # right frame - options - saturation
        self.__frmSaturation: "ttk.Frame" = None
        self.__lblSaturation: "ttk.Label" = None
        self.__spbSaturationMin: "ttk.Spinbox" = None
        self.__spbSaturationMax: "ttk.Spinbox" = None

        # right frame - options - intensity
        self.__frmIntensity: "ttk.Frame" = None
        self.__lblIntensity: "ttk.Label" = None
        self.__spbIntensityMin: "ttk.Spinbox" = None
        self.__spbIntensityMax: "ttk.Spinbox" = None

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
        title: "str" = "App",
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
        base_width = 300
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
        self.__spbHueShadowMin = ttk.Spinbox(master)
        self.__spbHueShadowMin.pack()

    def create_spb_hue_shadow_max(
        self,
        master
    ):
        self.__spbHueShadowMax = ttk.Spinbox(master)
        self.__spbHueShadowMax.pack()

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
        self.__spbHueLightMin = ttk.Spinbox(master)
        self.__spbHueLightMin.pack()

    def create_spb_hue_light_max(
        self,
        master
    ):
        self.__spbHueLightMax = ttk.Spinbox(master)
        self.__spbHueLightMax.pack()

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
        self.__spbSaturationMin = ttk.Spinbox(master)
        self.__spbSaturationMin.pack()

    def create_spb_saturation_max(
        self,
        master
    ):
        self.__spbSaturationMax = ttk.Spinbox(master)
        self.__spbSaturationMax.pack()

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
        self.__spbIntensityMin = ttk.Spinbox(
            master,
            command=self.update_spb_intensity_min
        )
        self.__spbIntensityMin.pack()

    def update_spb_intensity_min(
        self,
        value
    ):
        self.__scanner.lastIntensityMin = value
        self.__scanner.scan_image()
        self.__update_image_view()

    def create_spb_intensity_max(
        self,
        master
    ):
        self.__spbIntensityMax = ttk.Spinbox(
            master,
            command=self.update_spb_intensity_max
        )
        self.__spbIntensityMax.pack()
    
    def update_spb_intensity_max(
        self,
        value
    ):
        self.__scanner.lastIntensityMax = value
        self.__scanner.scan_image()
        self.__update_image_view()


system("cp output.bmp output_copy.bmp")

app = App(
    imagePath="output.bmp",
    title="Sakuga Scan",
    minWidth=0,
    minHeight=0,
    maxWidth=0,
    maxHeight=0
)

app.mainloop()

system("cp output_copy.bmp output.bmp")
system("rm output_copy.bmp")
