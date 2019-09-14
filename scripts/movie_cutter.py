import os
import time
import IPython
import ipywidgets as widgets
from termcolor import colored
from urllib.parse import urlparse
from moviepy.video.io.VideoFileClip import VideoFileClip


class MovieCutter(object):
    def __init__(self, movie_info, input_gdrive_path):
        self.out = widgets.Output()
        self.movie_info = movie_info
        self.input_gdrive_path = input_gdrive_path
        IPython.display.display(self.out)

    def widget(self):

        def on_value_change(change):
            start = self.start_slider.value
            end = self.end_slider.value
            with self.out:
                IPython.display.clear_output(wait=False)
                if start >= end:
                    print(colored("Start can't be greater than end", 'red'))
                    self.button_cut_movie.disabled = True
                else:
                    startstr = time.strftime('%H:%M:%S', time.gmtime(start))
                    endstr = time.strftime('%H:%M:%S', time.gmtime(end))
                    totalstr = time.strftime('%H:%M:%S', time.gmtime(end - start))
                    print(
                        "The movie will be cut from " + startstr + " to " + endstr + ", total time will be: " + totalstr)
                    self.button_cut_movie.disabled = False

        def on_click_cut_movie(b):
            with self.out:
                IPython.display.clear_output(wait=False)
                start = self.start_slider.value
                end = self.end_slider.value
                parsed = urlparse(self.movie_info.gdrivepath)
                basename = os.path.basename(parsed.path)
                newfilename = str(start) + "_" + str(end) + "_" + basename
                basenamewithoutextension, extension = os.path.splitext(basename)
                videofolderpath = self.input_gdrive_path + "/" + basenamewithoutextension
                mkdirforvideocommand = "mkdir -p '" + videofolderpath + "'"
                ret = os.system(mkdirforvideocommand)
                if ret == 0:
                    newfilepath = videofolderpath + "/" + newfilename
                    try:
                        with VideoFileClip(self.movie_info.gdrivepath) as video:
                            new = video.subclip(start, end)
                            new.write_videofile(newfilepath, audio_codec='aac')
                        self.movie_info.gdrivepath_after_cut = newfilepath
                        print(colored("Cutted video path: " + newfilepath, 'green'))
                    except:
                        print(colored("Exception: Not able to cut this movie.", 'red'))
                else:
                    print(colored("Exception: Not able to create folder for cutted file.", 'red'))

        box = widgets.VBox()

        self.start_slider = widgets.IntSlider(
            value=0,
            min=0,
            max=int(self.movie_info.length) - 1,
            step=1,
            description='Start:',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='d'
        )
        self.start_slider.observe(on_value_change, names='value')
        self.end_slider = widgets.IntSlider(
            value=int(self.movie_info.length),
            min=1,
            max=int(self.movie_info.length),
            step=1,
            description='End:  ',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='d'
        )
        self.end_slider.observe(on_value_change, names='value')
        self.button_cut_movie = widgets.Button(description="Cut movie")
        self.button_cut_movie.on_click(on_click_cut_movie)

        box.children = [self.start_slider, self.end_slider, self.button_cut_movie]
        return box