from os import system
from tkinter import (
	ttk, 
	IntVar,
	filedialog,
	Canvas,
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
from startup_config import config


class FrmImageView(Canvas):
	
	def __init__(
		self,
		master: "Misc",
		imagePath: "str"
	):
		super().__init__(
			master,
			width=500,
			height=700,
			background="gray75"
		)
		self.create_line(10, 5, 200, 500)
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
		dstDirectory = filedialog.asksaveasfilename(
			title="Save the image",
			initialdir="/",
			defaultextension=".bmp"
		)
		self.__imageView.save_image(dstDirectory)


class FrmImageOptions(ttk.Frame):

	def __init__(
		self,
		master,
		imageView: "FrmImageView",
		imageScanner: "ImageScanner",
		defaultValues: "dict" = {}
	):
		super().__init__(master)

		self.__imageView: "FrmImageView" = imageView
		self.__imageScanner: "ImageScanner" = imageScanner
		self.__defaultValues: "dict" = defaultValues

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
			intensityMaxCallback=self.__shadow_intensity_max_callback,
			hueMinDefault=self.__defaultValues.get("shadow_min_hue", 0),
			hueMaxDefault=self.__defaultValues.get("shadow_max_hue", 0),
			saturationMinDefault=self.__defaultValues.get("shadow_min_saturation", 0),
			saturationMaxDefault=self.__defaultValues.get("shadow_max_saturation", 0),
			intensityMinDefault=self.__defaultValues.get("shadow_min_intensity", 0),
			intensityMaxDefault=self.__defaultValues.get("shadow_max_intensity", 0)
		)
		self.__frmShadowOption.pack()
		self.__shadow_hue_min_callback()
		self.__shadow_hue_max_callback()
		self.__shadow_saturation_min_callback()
		self.__shadow_saturation_max_callback()
		self.__shadow_intensity_min_callback()
		self.__shadow_intensity_max_callback()

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
			intensityMaxCallback=self.__light_intensity_max_callback,
			hueMinDefault=self.__defaultValues.get("light_min_hue", 0),
			hueMaxDefault=self.__defaultValues.get("light_max_hue", 0),
			saturationMinDefault=self.__defaultValues.get("light_min_saturation", 0),
			saturationMaxDefault=self.__defaultValues.get("light_max_saturation", 0),
			intensityMinDefault=self.__defaultValues.get("light_min_intensity", 0),
			intensityMaxDefault=self.__defaultValues.get("light_max_intensity", 0)
		)
		self.__frmLightOption.pack()
		self.__light_hue_min_callback()
		self.__light_hue_max_callback()
		self.__light_saturation_min_callback()
		self.__light_saturation_max_callback()
		self.__light_intensity_min_callback()
		self.__light_intensity_max_callback()

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
			intensityMaxCallback=self.__line_intensity_max_callback,
			hueMinDefault=self.__defaultValues.get("line_min_hue", 0),
			hueMaxDefault=self.__defaultValues.get("line_max_hue", 0),
			saturationMinDefault=self.__defaultValues.get("line_min_saturation", 0),
			saturationMaxDefault=self.__defaultValues.get("line_max_saturation", 0),
			intensityMinDefault=self.__defaultValues.get("line_min_intensity", 0),
			intensityMaxDefault=self.__defaultValues.get("line_max_intensity", 0)
		)
		self.__frmLineOption.pack()
		self.__line_hue_min_callback()
		self.__line_hue_max_callback()
		self.__line_saturation_min_callback()
		self.__line_saturation_max_callback()
		self.__line_intensity_min_callback()
		self.__line_intensity_max_callback()

	def __shadow_hue_min_callback(
		self
	):
		self.__imageScanner.shadowScanner.lastHueMin = \
			self.__frmShadowOption.hueMin
		
	def __shadow_hue_max_callback(
		self
	):
		self.__imageScanner.shadowScanner.lastHueMax = \
			self.__frmShadowOption.hueMax
		
	def __shadow_saturation_min_callback(
		self
	):
		self.__imageScanner.shadowScanner.lastSaturationMin = \
			self.__frmShadowOption.saturationMin
		
	def __shadow_saturation_max_callback(
		self
	):
		self.__imageScanner.shadowScanner.lastSaturationMax = \
			self.__frmShadowOption.saturationMax
		
	def __shadow_intensity_min_callback(
		self
	):
		self.__imageScanner.shadowScanner.lastIntensityMin = \
			self.__frmShadowOption.intensityMin
		
	def __shadow_intensity_max_callback(
		self
	):
		self.__imageScanner.shadowScanner.lastIntensityMax = \
			self.__frmShadowOption.intensityMax

	def __light_hue_min_callback(
		self
	):
		self.__imageScanner.lightScanner.lastHueMin = \
			self.__frmLightOption.hueMin
		
	def __light_hue_max_callback(
		self
	):
		self.__imageScanner.lightScanner.lastHueMax = \
			self.__frmLightOption.hueMax
		
	def __light_saturation_min_callback(
		self
	):
		self.__imageScanner.lightScanner.lastSaturationMin = \
			self.__frmLightOption.saturationMin
		
	def __light_saturation_max_callback(
		self
	):
		self.__imageScanner.lightScanner.lastSaturationMax = \
			self.__frmLightOption.saturationMax
		
	def __light_intensity_min_callback(
		self
	):
		self.__imageScanner.lightScanner.lastIntensityMin = \
			self.__frmLightOption.intensityMin
		
	def __light_intensity_max_callback(
		self
	):
		self.__imageScanner.lightScanner.lastIntensityMax = \
			self.__frmLightOption.intensityMax

	def __line_hue_min_callback(
		self
	):
		self.__imageScanner.lineScanner.lastHueMin = \
			self.__frmLineOption.hueMin
		
	def __line_hue_max_callback(
		self
	):
		self.__imageScanner.lineScanner.lastHueMax = \
			self.__frmLineOption.hueMax
		
	def __line_saturation_min_callback(
		self
	):
		self.__imageScanner.lineScanner.lastSaturationMin = \
			self.__frmLineOption.saturationMin
		
	def __line_saturation_max_callback(
		self
	):
		self.__imageScanner.lineScanner.lastSaturationMax = \
			self.__frmLineOption.saturationMax
		
	def __line_intensity_min_callback(
		self
	):
		self.__imageScanner.lineScanner.lastIntensityMin = \
			self.__frmLineOption.intensityMin
		
	def __line_intensity_max_callback(
		self
	):
		self.__imageScanner.lineScanner.lastIntensityMax = \
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
		intensityMaxCallback: "function",
		hueMinDefault: "int" = 0,
		hueMaxDefault: "int" = 0,
		saturationMinDefault: "int" = 0,
		saturationMaxDefault: "int" = 0,
		intensityMinDefault: "int" = 0,
		intensityMaxDefault: "int" = 0,
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
		self.__create_frm_hue_min(hueMinCallback, hueMinDefault)
		self.__create_frm_hue_max(hueMaxCallback, hueMaxDefault)
		self.__create_frm_saturation_min(
			saturationMinCallback, saturationMinDefault)
		self.__create_frm_saturation_max(
			saturationMaxCallback, saturationMaxDefault)
		self.__create_frm_intensity_min(
			intensityMinCallback, intensityMinDefault)
		self.__create_frm_intensity_max(
			intensityMaxCallback, intensityMaxDefault)

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
		callback: "function",
		default: "int"
	):
		self.__frmHueMin = FrmImageOptionProperty(
		 self,
			name="Hue min.:",
			minValue=0,
			maxValue=HUE_MAX,
			callback=callback,
			imageView=self.__imageView,
			imageScanner=self.__imageScanner,
			defaultValue=default
		)
		self.__frmHueMin.grid(
			column=0,
			row=1
		)

	def __create_frm_hue_max(
		self,
		callback: "function",
		default: "int"
	):
		self.__frmHueMax = FrmImageOptionProperty(
			self,
			name="Hue max.:",
			minValue=0,
			maxValue=HUE_MAX,
			callback=callback,
			imageView=self.__imageView,
			imageScanner=self.__imageScanner,
			defaultValue=default
		)
		self.__frmHueMax.grid(
			column=0,
			row=2
		)

	def __create_frm_saturation_min(
		self,
		callback: "function",
		default: "int"
	):
		self.__frmSaturationMin = FrmImageOptionProperty(
			self,
			name="Sat. min.:",
			minValue=0,
			maxValue=SATURATION_MAX,
			callback=callback,
			imageView=self.__imageView,
			imageScanner=self.__imageScanner,
			defaultValue=default
		)
		self.__frmSaturationMin.grid(
			column=1,
			row=1
		)

	def __create_frm_saturation_max(
		self,
		callback: "function",
		default: "int"
	):
		self.__frmSaturationMax = FrmImageOptionProperty(
			self,
			name="Sat. max.:",
			minValue=0,
			maxValue=SATURATION_MAX,
			callback=callback,
			imageView=self.__imageView,
			imageScanner=self.__imageScanner,
			defaultValue=default
		)
		self.__frmSaturationMax.grid(
			column=1,
			row=2
		)

	def __create_frm_intensity_min(
		self,
		callback: "function",
		default: "int"
	):
		self.__frmIntensityMin = FrmImageOptionProperty(
			self,
			name="Int. min.:",
			minValue=0,
			maxValue=INTENSITY_MAX,
			callback=callback,
			imageView=self.__imageView,
			imageScanner=self.__imageScanner,
			defaultValue=default
		)
		self.__frmIntensityMin.grid(
			column=2,
			row=1
		)

	def __create_frm_intensity_max(
		self,
		callback: "function",
		default: "int"
	):
		self.__frmIntensityMax = FrmImageOptionProperty(
			self,
			name="Int. max.:",
			minValue=0,
			maxValue=INTENSITY_MAX,
			callback=callback,
			imageView=self.__imageView,
			imageScanner=self.__imageScanner,
			defaultValue=default
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
		imageScanner: "ImageScanner",
		defaultValue: "int" = 0   
	):
		super().__init__(master)

		self.__callback = callback
		self.__imageView: "FrmImageView" = imageView
		self.__imageScanner: "ImageScanner" = imageScanner
		self.__defaultValue: "int" = defaultValue

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
		self.__varPropertyValue = IntVar(
			self,
			value=self.__defaultValue
		)

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
			imageScanner=self.__imageScanner,
			defaultValues=config
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
