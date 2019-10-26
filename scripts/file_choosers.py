import os
import math
import IPython
import ipywidgets as widgets
from termcolor import colored
from moviepy.editor import VideoFileClip


class FileBrowser(object):
    def __init__(self, info, path=None):
        self.out = widgets.Output()
        IPython.display.display(self.out)
        self.info = info
        if path is None:
            self.path = os.getcwd()
        else:
            self.path = path
        self._update_files()

    def _update_files(self):
        self.files = list()
        self.dirs = list()
        self.dirs.append("..")
        if os.path.isdir(self.path):
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
            self.check_file()

        box.children = [widgets.HTML("<h2>%s</h2>" % (self.path,))] + hboxes

    def check_file(self):
        pass


class ImageBrowser(FileBrowser):
    def __init__(self, info, path=None):
        FileBrowser.__init__(self, info, path)

    def check_file(self):
        try:
            IPython.display.display(IPython.display.Image(self.path, width=500))
            self.info.gdrivepath = self.path
        except:
            print(colored("Choose image.", 'red'))


class VideoBrowser(FileBrowser):
    def __init__(self, info, path=None):
        FileBrowser.__init__(self, info, path)

    def check_file(self):
        try:
            clip = VideoFileClip(self.path)
            print(colored("You've chosen video: " + self.path, 'green'))
            self.info.gdrivepath = self.path
            self.info.length = int(clip.duration)
        except:
            print(colored("Choose video.", 'red'))
