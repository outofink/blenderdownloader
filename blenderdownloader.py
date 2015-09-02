from bs4 import BeautifulSoup as BS
import sys, getopt, zipfile
from os import system, name, path, remove

if sys.version_info.major == 3:
	import urllib.request, urllib.error
	urlopen   = urllib.request.urlopen
	Request   = urllib.request.Request
	HTTPError =	urllib.error.HTTPError
	URLError  = urllib.error.URLError
elif sys.version_info.major == 2:
	import urllib2
	urlopen   = urllib2.urlopen
	Request   = urllib2.Request
	HTTPError =	urllib2.HTTPError
	URLError  = urllib2.URLError

class BlenderDownloader():
	def __init__(self, argv):
		self.main(argv)

	def main(self, argv):
		opts, args = getopt.getopt(argv, "hv:", ["help", "version="])
		grammar = ""
		for opt, arg in opts:                
			if opt in ("-h", "--help"):
				print("You thought there was help!? Well, there will be soon.")                          
				sys.exit()                                    
			elif opt in ("-v", "--version"):
				grammar = arg
		system('cls' if name == 'nt' else 'clear')
		print("Blender Downloader v1.0")
		print("Retrieving most recent Blender version...")
		try:
			blender_html = BS(urlopen(Request('http://www.blender.org')).read(), "html.parser")
		except URLError:
			print("\nERROR: Not connected to the internet.")
			sys.exit(1)
		blenderCurVer = blender_html.find('button', attrs={'class':"btn btn-default btn-lg"}).text.strip()
		print("\nMost recent version is %s." % blenderCurVer)
		#blenderCurVerNum = float(blenderCurVer.replace("Blender ",""))
		def genlink(version=blenderCurVer.replace("Blender ",""), platform="windows64"):
			gversion=version.replace("a","").replace("b","")

			final="http://download.blender.org/release/Blender{0}/blender-{2}-{1}.zip".format(gversion, platform, version)
			try:
				u = urlopen(final)
			except HTTPError:
				try:
					final="http://download.blender.org/release/Blender{0}/blender-{2}-release-{1}.zip".format(gversion, platform, version)
					u = urlopen(final)
				except HTTPError:
					print("ERROR: Blender version does not exist.\nNote: Blender Downloader only supports Blender 2.57+")
					return False
				return final
			return final	
		def download(link):
			file_name = link.split('/')[-1]
			u = urlopen(link)
			f = open(file_name, 'wb')
			meta = u.info()
			file_size = int(meta["Content-Length"])
			file_sizeMB=file_size/1024.0/1024.0
			print("Downloading: {0} filesize: {1:.4}MB".format(file_name, file_sizeMB))
			file_size_dl = 0
			block_sz = 1024
			while True:
			    buffer = u.read(block_sz)
			    if not buffer:
			        break
			    file_size_dl += len(buffer)
			    f.write(buffer)
			    p = float(file_size_dl) / file_size
			    status = r"{0:.2f}MB/{2:.2f}MB [{1:.2%}]       ".format(file_size_dl/1024.0/1024.0, p, file_sizeMB)
			    status = status + chr(8)*(len(status)+1)
			    sys.stdout.write(status)
			print()
			f.close()
			return file_name
		def extract(zipped="blender-2.70-windows64.zip"):
			zip = zipfile.ZipFile(zipped)
			nameList = zip.namelist()
			fileCount = len(nameList)
			print("\nExtracting: %s filecount: %s files" % (zipped, fileCount))
			count = 0
			for item in nameList:
				count += 1
				dir,file = path.split(item)
				lolz =r"{0}/{1} files unzipped [{2:.2%}]".format(count, fileCount, (count*1.0)/fileCount)
				lolz = lolz + chr(8)*(len(lolz)+1)
				sys.stdout.write(lolz) 
				zip.extract(item,"")
			print()
			return True
		if grammar:
			linked=genlink(grammar)
		else:
			linked=genlink()
		if linked:
			if grammar:
				print("Downloading Blender %s now... (please wait a bit)\n" % grammar)
			else:
				print("Downloading most recent version now... (please wait a bit)\n")
			blenderzip=download(linked)
			print("\nExtracting blender package...")
			#other stuff
			extract(blenderzip)
			print("\nCleaning up...")
			remove(blenderzip)
			print("\nDone!")

if __name__ == "__main__":
	BlenderDownloader(sys.argv[1:])
