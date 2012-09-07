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
import Image, ImageDraw, ImageFont

class mediaI:
    """
    This class determines and stores the following metadata: aspect ratio, duration, bitrate and dimensions. 
    """
    
    filesize = 0
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

        # parse filesize
        fs_start = data.find(":", data.find("File size")) + 2 
        fs_end = data.find("\n",fs_start)
        self.filesize = data[fs_start:fs_end]

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

        wi_num = width[0:width.find("p", 0) - 1]     
        he_num = heigth[0:heigth.find("p", 0) - 1]  
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
    # montage 47/*.jpeg -geometry $GEOM -tile $TILE 47/montage.jpg
    
    files = os.listdir(path)
    files.sort()
    counter = 0      # images
    counter2 = 0     # montages
    tile = "3x3"
    param = []

    if mi.aspect_ratio == "4:3":
        geom = "480x360+2+2"
    elif mi.aspect_ratio == "3:2":
        geom  = "480x320+2+2"
    else:
        geom = "640x360+2+2"
    
    # remove the videofile from the list
    for file in files:
        if file.find("jpeg", 0) == -1:
            files.pop(files.index(file))
        
    size = len(files)
    n_mon = size/9
    mod_mon = size % 9
 
    # first create the full montages
    while counter < n_mon*9:
        # build the subprocess's parameterlist
        param.append("montage")
        for n in range(9):
            param.append(os.path.join(path,files[counter]))
            counter = counter + 1
        param.append("-geometry")
        param.append(geom)
        param.append("-tile")
        param.append(tile)
        param.append(os.path.join(path, "montage-" + str(counter2) + ".jpg"))
        counter2 = counter2 + 1;
        
        try:
            subprocess.call(param)
        except subprocess.CalledProcessError as e:
            sys.exit(e.output)
        except OSError as e:
            sys.exit(e.strerror)
        
        param[:] = []
    
    # then the last
    if mod_mon <> 0:
        # build subprocess's paremeterlist
        param.append("montage")
        while counter < len(files):
            param.append(os.path.join(path,files[counter]))
            counter = counter + 1
        param.append("-geometry")
        param.append(geom)
        param.append("-tile")
        param.append(tile)
        param.append(os.path.join(path, "montage-" + str(counter2) + ".jpg"))

        try:
            subprocess.call(param)
        except subprocess.CalledProcessError as e:
            sys.exit(e.output)
        except OSError as e:
            sys.exit(e.strerror)
        
        param[:] = []

def create_header(filename, mi):
    """
    Uses the Python Imaging Library. (PIL)
    """
    
    ff = "/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf"
    tab = 150
    row = 17
    y = 5
    sy = 110

    # create the image
    color = (255, 255, 255)
    if mi.aspect_ratio == "3:2":
        size = 1452, sy
    elif mi.aspect_ratio == "4:3":
        size = 1452, sy
    else:
        size = 1932, sy

    header = Image.new("RGB", size, color)

    # draw text into the image
    draw = ImageDraw.Draw(header)
    try:
        font = ImageFont.truetype(ff, 14)
    except IOError as e:
        print "Cannot find font: " + ff
        sys.exit(e.strerror)
    
    draw.text((5, y), "file", font = font, fill = "black")
    draw.text((tab, y), ":" + filename, font = font, fill = "black")
    y = y + row
    draw.text((5, y), "filesize", font = font, fill = "black")
    draw.text((tab, y), ":" + mi.filesize, font = font, fill = "black")
    y = y + row
    draw.text((5, y), "aspect ratio", font = font, fill = "black")
    draw.text((tab, y), ":" + mi.aspect_ratio, font=font, fill = "black")
    y = y + row
    draw.text((5, y), "Dimensions", font = font, fill = "black")
    draw.text((tab, y), ":" + mi.dimensions, font = font, fill = "black")
    y = y + row
    draw.text((5, y), "Bitrate", font = font, fill = "black")
    draw.text((tab, y), ":" + mi.bit_rate, font = font, fill = "black")
    y = y + row
    draw.text((5, y), "Duration", font = font, fill = "black")
    draw.text((tab, y), ":" + mi.duration_pr, font = font, fill = "black")

    return header
    
def join_images(path, mi, header):
    """
    Attaches the headerimage on top of the montages.
    Uses PIL.
    """

    counter = 0
    h_y = 110 # header y-size
    color = (255, 255, 255)

    if mi.aspect_ratio == "3:2":
        im_x = 1452
        im_y = 972 + h_y
    elif mi.aspect_ratio == "4:3":
        im_x = 1452
        im_y = 1092 + h_y
    else:
        im_x = 1932
        im_y = 1092 + h_y

    im_size = im_x, im_y

    files = os.listdir(path)
    files.sort()

    # join header with montages
    for file in files:
        if file.find("montage", 0) <> -1:
            im = Image.new("RGB", im_size, color)
            try:
                mn = Image.open(os.path.join(path, file))
            except IOerror as e:
                sys.exit(e.output)
            except OSError as e:
                sys.exit(e.strerror)
            im.paste(header, (0,0))
            im.paste(mn, (0, h_y + 1))
            try:
                im.save(os.path.join(path, file), "JPEG")
            except IOerror as e:
                sys.exit(e.output)
            except OSError as e:
                sys.exit(e.strerror)
            counter = counter + 1

def cleanup(path):
    """
    Deletes temporary files.
    """
    
    files = os.listdir(path)
    
    for file in files:
        if file.find("image",0) <> -1:
            os.remove(os.path.join(path, file))

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
    header= create_header(filename, mi)
    join_images(path, mi, header)
    cleanup(path)
        
if __name__ == "__main__":
        main()
