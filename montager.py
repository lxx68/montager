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
    This class determines and stores the following metadata: aspect ratio, duration, bitrate and dimensions. 
    """
    
    aspect_ratio = ""
    duration_pr = ""   # printable version
    duration = 0       # in seconds
    bit_rate = ""
    dimensions = ""

    def __init__(self, file):
        data = self.read_mediainfo(file)
        self.fill_variables(data)
        pass

    def read_mediainfo(self, file):
        """
        Uses mediainfo.
        """
        try:
           data= subprocess.check_output(["mediainfo", file])
        except CalledProcessError as e:
            sys.exit(e.output)
        except OSError as e:
            sys.exit(e.strerror)

        return data

    def fill_variables(self, data):
        """
        Fills the member variables based on the data.
        """

        # parse aspect ratio
        ar_start = data.find(":", data.find("Display aspect ratio")) + 2 
        ar_end = data.find("\n",ar_start)
        self.aspect_ratio = data[ar_start:ar_end]

        # parse duration and duration_pr
        # parse dur_raw
        dur_raw_start = data.find(":", data.find("Duration")) + 2 
        dur_raw_end = data.find("\n",dur_raw_start)
        dur_raw = data[dur_raw_start:dur_raw_end]

        self.duration_pr = dur_raw

        # set hour flag
        if dur_raw.find("h", 0) <> -1:
            hour_flag = True
        else:
            hour_flag = False

        # parse hours
        if hour_flag:
            dur_hour_end = data.find("h", dur_raw_start) 
            dur_hour =  int(data[dur_raw_start:dur_hour_end])

        # parse minutes
        dur_min_end = data.find("m", dur_raw_start)
        if not hour_flag:
            dur_min = int(data[dur_raw_start:dur_min_end])
        else:
            dur_min = int(data[dur_hour_end+2:dur_min_end])

        # parse seconds
        if not hour_flag:
            dur_sec_start = data.find(" ", dur_min_end) + 1
            dur_sec = int(data[dur_sec_start:dur_raw_end - 1])

        # calculate total duration in seconds
        if not hour_flag:
            self.duration = dur_min*60 + dur_sec
        else:
            self.duration = (dur_hour*60 + dur_min) * 60

        # parse bitrate
        br_start = data.find(":", data.find("Bit rate")) + 2 
        br_end = data.find("\n",br_start)
        self.bit_rate = data[br_start:br_end]

        # parse dimensions
        wi_start = data.find(":", data.find("Width")) + 2 
        wi_end = data.find("\n",wi_start)
        width = data[wi_start:wi_end]

        he_start = data.find(":", data.find("Height")) + 2 
        he_end = data.find("\n",he_start)
        heigth = data[he_start:he_end]

        wi_num = width[0:width.find(" ", 0)]
        he_num = heigth[0:heigth.find(" ", 0)]
        self.dimensions = wi_num + "x" + he_num + " pixels"

# the main program

def extract_images(path, filename):
    """
    Extracts a frame from the video file every 10 seconds.
    Uses ffmpeg.
    """
    # ffmpeg -i infile -r framerate -f image2 outfile

    infile = os.path.join(path, filename)
    framerate = "0.1"
    format = "image2"
    output = path + "/image-%3d.jpeg"

    try:
       subprocess.call(["ffmpeg",
                        "-i" ,infile, 
                        "-r" ,framerate, 
                        "-f", 
                        format, 
                        output])
    except subprocess.CalledProcessError as e:
        sys.exit(e.output)
    except OSError as e:
        sys.exit(e.strerror)

def create_montages(path, mi):
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
    file = args.file
    (path, filename) = os.path.split(file)
    
    if not os.path.exists(file):
        sys.exit("File does not exist!")

    if not os.path.isfile(file):
        sys.exit("File is a folder!")
        
    mi = mediaI(file)
    extract_images(path, filename)
    create_montages(path, mi)
    create_header(path, mi)
    join_images(path)
    cleanup(path)
        
if __name__ == "__main__":
        main()
