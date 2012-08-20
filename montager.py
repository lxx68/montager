#!/usr/bin/python
""" montager.py
Creates montage images of every 10 seconds from the selected video file.
Images are named as 'montage-...' and placed into same folder with the video.
usage: montager.py [-h] file

positional arguments:
  file        Video file

optional arguments:
  -h, --help  show this help message and exit
"""

import sys
import argparse
import os.path
import subprocess

class mediaI:
    """
    This class determines and stores the following metadata: aspect ratio and runtime. 
    """
    def __init__(self, path):
        xml = self.read_mediainfo(path)
        self.fill_variables(xml)
        pass

    def read_mediainfo(self, path):
        """
        Gets videofiles metadata in XML -format.
        Uses mediainfo.
        """
        try:
           xml= subprocess.check_output(["mediainfo", "--Output=XML", path])
        except CalledProcessError as e:
            sys.exit(e.output)
        except OSError as e:
            sys.exit(e.strerror)

        return xml

    def fill_variables(self, xml):
        """
        Fills the member variables based on the XML.
        Uses Elementtree- package.
        """
        pass

# the main program

def extract_images(path):
    """
    Extracts a frame from the video file every 10 seconds.
    Uses ffmpeg.
    """
    pass

def create_montages(path):
    """
    Uses ImageMagick's montage -tool.
    """
    pass

def create_header(path, mi):
    """
    Uses the Python Imaging Library. (PIL)
    """
    pass

def join_images(path):
    """
    Attaches the headerimage on top of the montages.
    Uses PIL.
    """
    pass

def cleanup(path):
    """
    Deletes temporary files.
    """
    pass

def main():
        
    argparser = argparse.ArgumentParser()
    argparser.add_argument("file", help="Video file")
    args = argparser.parse_args()
    path = args.file
    
    if not os.path.exists(path):
        sys.exit("File does not exist!")

    if not os.path.isfile(path):
        sys.exit("File is a folder!")
        
    mi = mediaI(path)
    extract_images(path)
    create_montages(path)
    create_header(path, mi)
    join_images(path)
    cleanup(path)
        
if __name__ == "__main__":
        main()
