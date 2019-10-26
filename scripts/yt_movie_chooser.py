import ipywidgets as widgets
from pytube import YouTube
from urllib.parse import urlparse
from termcolor import colored
import IPython
import os


class YTMovieChooser(object):
    def __init__(self, movie_info, input_gdrive_path):
        self.out = widgets.Output()
        self.movie_info = movie_info
        self.input_gdrive_path = input_gdrive_path
        IPython.display.display(self.out)

    def widget(self):

        dropdown_info = 'Load streams firstly'

        def stream_to_label(stream):
            res = stream.resolution or "Unknown resolution"
            mt = stream.mime_type or "Unknown type"
            return res + " " + mt

        def on_click_load_streams(b):
            with self.out:
                IPython.display.clear_output(wait=False)
                try:
                    yt = YouTube(self.text.value)
                    streams = yt.streams.filter(only_video=True, file_extension='mp4').all()
                    labels = list(map(stream_to_label, streams))
                    self.streams = dict(zip(labels, streams))
                    print(colored("Your video title: " + yt.title, 'green'))  # Not working sometimes
                    self.dropdown.options = labels
                    self.dropdown.value = labels[0]
                    self.dropdown.disabled = False
                    self.button_load_movie.disabled = False
                    self.yt = yt
                except:
                    print(colored("Exception: Problem with YT URL", 'red'))
                    self.dropdown.options = [dropdown_info]
                    self.dropdown.value = dropdown_info
                    self.dropdown.disabled = True
                    self.button_load_movie.disabled = True

        def on_click_download_movie(b):
            with self.out:
                IPython.display.clear_output(wait=False)
                label = self.dropdown.value
                stream = self.streams[label]
                try:
                    print("Trying to download your video")
                    filepath = stream.download()
                    parsed = urlparse(filepath)
                    basename = os.path.basename(parsed.path)
                    res = self.dropdown.value.split()[0]
                    newfilename = res + "_" + basename
                    basenamewithoutextension, extension = os.path.splitext(basename)
                    videofolderpath = self.input_gdrive_path + "/" + res + "_" + basenamewithoutextension
                    mkdirforvideocommand = "mkdir -p '" + videofolderpath + "'"
                    ret = os.system(mkdirforvideocommand)
                    if ret == 0:
                        print(colored("Directory is created: " + videofolderpath, 'green'))
                        newfilepath = videofolderpath + "/" + newfilename
                        mvvideocommand = "mv '" + filepath + "' '" + newfilepath + "'"
                        ret = os.system(mvvideocommand)
                        if ret == 0:
                            print(colored("Downloaded to: " + newfilepath, 'green'))
                            self.movie_info.gdrivepath = newfilepath
                            self.movie_info.length = int(self.yt.length)
                        else:
                            print(colored("Exception: Something went wrong while copying movie to your drive.", 'red'))
                    else:
                        print(colored(
                            "Problem with creating folder for video: " + videofolderpath + "   Make sure you mounted gdrive",
                            'red'))
                except Exception as e:
                    print(colored("Exception: Not able to download this movie. Try with other url.", 'red'))
                    print(colored(e, 'red'))

        box = widgets.VBox()
        self.text = widgets.Text(
            value="",
            description='YT URL: ',
            disabled=False
        )
        self.button_load_streams = widgets.Button(description="Load streams")
        self.button_load_streams.on_click(on_click_load_streams)

        self.dropdown = widgets.Dropdown(
            options=[dropdown_info],
            value=dropdown_info,
            description='Stream:',
            disabled=True,
        )
        self.button_load_movie = widgets.Button(description="Download video", disabled=True)
        self.button_load_movie.on_click(on_click_download_movie)

        box.children = [self.text, self.button_load_streams, self.dropdown, self.button_load_movie]
        return box