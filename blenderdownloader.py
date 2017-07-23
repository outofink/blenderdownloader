"""
blenderdownloader v2
Automatically downloads the latest version of Blender.
"""

import os
import sys
import zipfile

import requests
from bs4 import BeautifulSoup

class BlenderDownloader():
    """Automatically downloads the latest version of Blender."""
    def __init__(self):
        self.link = ""
        self.filename = ""
        self.version = ""

    def getnewestversion(self):
        """Gets download link, filename, and version of the newest version of Blender."""
        page = requests.get('https://www.blender.org/download/')
        parsed = BeautifulSoup(page.text, 'html.parser')
        version = parsed.find('h2', attrs={'class':""}).text[-5:].strip()
        self.getversion(version)

    def getversion(self, version):
        self.version = version
        self.link = "http://download.blender.org/release/Blender{0}/blender-{1}-windows64.zip".format(version[:4], version)

        test = requests.get(self.link, stream=True)
        if test.headers['Content-Type'] != 'application/zip':
            print("Bad link.")
            sys.exit(1)

        self.filename = self.link.split('/')[-1]

    def download(self):
        """Downloads the newest build of Blender."""
        link = self.link
        filename = self.filename
        with open(filename, 'wb') as archive:
            print("Downloading {}...".format(filename))
            response = requests.get(link, stream=True)
            total = response.headers.get('content-length')

            downloaded = 0
            total = int(total)/1024/1024 # in MB
            for data in response.iter_content(chunk_size=4096):
                downloaded += len(data)/1024/1024 # in MB
                archive.write(data)
                percent = str(int(100 * downloaded / total)).rjust(3)
                percentbar = '[{}]'.format(('=' * int(int(percent)/2)).ljust(50))
                progress = f'\r{percent}% {percentbar} {downloaded:.2f}MB/{total:.2f}MB'
                sys.stdout.write(progress)
                sys.stdout.flush()
        print() # to add a newline

    def extract(self):
        """Extracts the newest build of Blender."""
        unzipper = zipfile.ZipFile(self.filename)
        nameList = unzipper.namelist()
        total = len(nameList)
        print("Extracting {}...".format(self.filename))
        for count, item in enumerate(nameList):
            percent = str(int(100 * count / total)).rjust(3)
            percentbar = '[{}]'.format(('=' * int(int(percent)/2)).ljust(50))
            progress = f'\r{percent}% {percentbar} {count+1}/{total}\n'
            sys.stdout.write(progress)
            sys.stdout.flush()

            unzipper.extract(item)
        print()

    def cleanup(self):
        """Removes unnecessary files."""
        print("Cleaning up...")
        os.remove(self.filename)

if __name__ == "__main__":
    blenderdownloader = BlenderDownloader()

    os.system("cls")
    print("Blender Downloader v2")
    print("Retrieving most recent Blender build version...")

    blenderdownloader.getnewestversion()

    print("Most recent version is Blender {}.".format(blenderdownloader.version))

    if os.path.isfile(blenderdownloader.filename[:-4] + "/version.txt"):
        with open(blenderdownloader.filename[:-4] + "/version.txt", "r") as text:
            if text.readline() >= blenderdownloader.version:
                print("Blender is up to date!")
                sys.exit(0)

    blenderdownloader.download()
    blenderdownloader.extract()
    blenderdownloader.cleanup()

    with open(blenderdownloader.filename[:-4] + "/version.txt", "w") as version:
            version.write(blenderdownloader.version)
