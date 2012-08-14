#!/usr/bin/python

import sys

class mediaI:
    def __init__(self, path):
        xml = self.read_mediainfo(path)
        self.fill_variables(xml)
        pass

    def read_mediainfo(self, path):
        pass

    def fill_variables(self, xml):
        pass

# the main program

def extract_images(path):
    pass

def create_montages(path):
    pass

def create_header(path, mi):
    pass

def join_images(path):
    pass

def cleanup(path):
    pass

def main():
        path = sys.argv[1]
        mi = mediaI(path)
        extract_images(path)
        create_montages(path)
        create_header(path, mi)
        join_images(path)
        cleanup(path)
        
if __name__ == "__main__":
        main()

