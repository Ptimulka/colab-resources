import os
import uuid
import IPython
import ipywidgets as widgets
from termcolor import colored
from urllib.parse import urlparse


class URLBrowser(object):
    def __init__(self, image_info, input_gdrive_path):
        self.out = widgets.Output()
        self.image_info = image_info
        self.input_gdrive_path = input_gdrive_path
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
        wgetcommand = "wget --quiet -P '" + self.input_gdrive_path + "' " + url
        ret = os.system(wgetcommand)
        if ret == 0:
            newfilefrompath = self.input_gdrive_path + "/" + basename
            newfiletopath = self.input_gdrive_path + "/" + newfilename
            mvcommand = "mv '" + newfilefrompath + "' '" + newfiletopath + "'"
            retmv = os.system(mvcommand)
            if retmv == 0:
                print(colored("Downloaded file path: " + newfiletopath, 'green'))
            else:
                print(colored("Exception: Problem with mving the file", 'red'))
        else:
            print(colored("Exception: Problem with downloading the file", 'red'))