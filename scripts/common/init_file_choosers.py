class FileBrowser(object):
    def __init__(self, image_info, path=None):
        self.out = widgets.Output()
        IPython.display.display(self.out)
        self.image_info = image_info
        if path == None:
            self.path = os.getcwd()
        else:
            self.path = path
        self._update_files()

    def _update_files(self):
        self.files = list()
        self.dirs = list()
        self.dirs.append("..")
        if (os.path.isdir(self.path)):
            for f in os.listdir(self.path):
                ff = self.path + "/" + f
                if os.path.isdir(ff):
                    self.dirs.append(f)
                else:
                    self.files.append(f)

    def widget(self):
        box = widgets.VBox()
        self._update(box)
        return box

    def _update(self, box):

        def on_click(b):
            if b.description == '..':
                self.path = os.path.split(self.path)[0]
            else:
                self.path = self.path + "/" + b.description
            self._update_files()
            self._update(box)

        buttons = []
        width = 5
        hboxes = []
        hboxes_len = math.ceil((len(self.dirs) + len(self.files)) / width)
        for i in range(hboxes_len):
            hboxes.append(widgets.HBox())
        hboxes_children = [[] for i in range(hboxes_len)]
        i = 0
        for f in self.dirs:
            button = widgets.Button(description=f, button_style='warning')
            button.on_click(on_click)
            hboxes_children[math.floor(i / width)].append(button)
            i += 1
        for f in self.files:
            button = widgets.Button(description=f)
            button.on_click(on_click)
            hboxes_children[math.floor(i / width)].append(button)
            i += 1
        for hbox, children in zip(hboxes, hboxes_children):
            hbox.children = children

        with self.out:
            IPython.display.clear_output(wait=False)
            try:
                IPython.display.display(IPython.display.Image(self.path, width=500))
                self.image_info.gdrivepath = self.path
            except:
                print("Choose image")

        box.children = [widgets.HTML("<h2>%s</h2>" % (self.path,))] + hboxes


class URLBrowser(object):
    def __init__(self, image_info):
        self.out = widgets.Output()
        self.image_info = image_info
        IPython.display.display(self.out)
        self.url = ''

    def widget(self):

        def on_click(b):
            with self.out:
                IPython.display.clear_output(wait=False)
                if (self.is_valid_url(self.text.value)):
                    try:
                        IPython.display.display(IPython.display.Image(self.text.value, width=500))
                        gdrive_path = self.download_to_gdrive(self.text.value)
                        self.image_info.gdrivepath = gdrive_path
                    except:
                        print(colored("Exception: Not image URL", 'red'))
                else:
                    print(colored("Not image URL", 'red'))

        box = widgets.VBox()
        self.button = widgets.Button(description="Load image")
        self.button.on_click(on_click)
        self.text = widgets.Text(
            value="",
            description='Image URL: ',
            disabled=False
        )
        box.children = [self.text, self.button]
        return box

    def is_valid_url(self, url):
        parsed = urlparse(url)
        return (parsed.scheme and parsed.netloc)

    def download_to_gdrive(self, url):
        parsed = urlparse(url)
        basename = os.path.basename(parsed.path)
        newfilename = str(uuid.uuid4()) + basename
        !wget --quiet - P
        "$input_gdrive_path" $url
        newfilefrompath = input_gdrive_path + "/" + basename
        newfiletopath = input_gdrive_path + "/" + newfilename
        !mv "$newfilefrompath" "$newfiletopath"
        return newfiletopath


def upload_file(image_info):
    from google.colab import files
    uploaded = files.upload()

    if (len(uploaded.keys()) != 0):
        filename = next(iter(uploaded.keys()))
        newfilename = str(uuid.uuid4()) + filename

        !mv "$filename" "$newfilename"
        !mv "$newfilename" "$input_gdrive_path"

        image_info.gdrivepath = input_gdrive_path + "/" + newfilename


class ImageSizeChooser(object):
    def init_recommended(self):
        try:
            width, height = load_img_size(image_info.gdrivepath, 1)
            with self.out:
                self.original_info = "Original image size is: " + str(width) + "x" + str(height)
                longer = max(width, height)
                recommended_longer = 512
                if (longer > recommended_longer):
                    self.recommended_scale = round(100 * float(recommended_longer) / longer)
                    self.recommended_info = colored(
                        "We recommend to change image size to " + str(self.recommended_scale) + "%", 'green')
                else:
                    self.recommended_scale = 100
        except:
            print(colored("Error occured, probably the image is not selected.", 'red'))

    def __init__(self, image_info):
        self.out = widgets.Output()
        self.image_info = image_info
        IPython.display.display(self.out)
        self.init_recommended()

    def widget(self):

        def on_click_custom_scale(b):
            with self.out:
                IPython.display.clear_output(wait=False)
                try:
                    print(self.original_info)
                    if (self.recommended_info is not None):
                        print(self.recommended_info)
                    print(colored("Scale set to " + str(self.scale_slider.value) + "%", 'green'))
                    width, height = load_img_size(image_info.gdrivepath, float(self.scale_slider.value) / 100)
                    print("Image size: " + str(width) + "x" + str(height))
                    IPython.display.display(IPython.display.Image(image_info.gdrivepath, width=width))
                    self.image_info.scale = self.scale_slider.value
                except:
                    print(colored("Error occured, probably the image is not selected.", 'red'))

        self.scale_slider = widgets.IntSlider(
            value=self.recommended_scale,
            min=5,
            max=100,
            step=1,
            description='Scale:',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='d'
        )

        box = widgets.VBox()
        self.button = widgets.Button(description="Apply scale")
        self.button.on_click(on_click_custom_scale)
        box.children = [self.scale_slider, self.button]
        on_click_custom_scale(self.button)
        return box