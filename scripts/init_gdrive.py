import os
from termcolor import colored

input_gdrive_path = "/content/gdrive/My Drive/ArtisticGoogleColabs/input"
output_gdrive_path = "/content/gdrive/My Drive/ArtisticGoogleColabs/output"
styles_gdrive_path = "/content/gdrive/My Drive/ArtisticGoogleColabs/styles"


def make_dir(path):
    mkdir_command = "mkdir -p '" + path + "'"

    ret = os.system(mkdir_command)
    if ret == 0:
        print(colored("Folder is created: " + path, 'green'))
    else:
        print(colored("Problem with creating folder: " + path + "   Make sure you mounted gdrive", 'red'))


make_dir(input_gdrive_path)
make_dir(output_gdrive_path)
make_dir(styles_gdrive_path)