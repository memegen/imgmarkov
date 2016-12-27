"""
import.py
Converts an image to data readable by imgmarkov.py

usage: python import.py [<file>]

"""

from PIL import Image
import sys

# reads the image pixel by pixel saves to file
def importimg(path):
	im = Image.open(path)
	w, h = im.size
	px = im.load()

	print str(w)+"x"+str(h)+" image imported."
	f1 = open('data/indat.txt','w')
	out = str(w)+"x"+str(h)+";"

	for i in range(0,h):
		for j in range(0,w):
			r, g, b = px[j,i][:3]
			#print r,g,b,a
			out += str(r)+","+str(g)+","+str(b)+";"

	f1.write(out)
	print "saved."

if __name__ == "__main__":
	path = "images/img2.png"
	if len(sys.argv) > 1:
		path = sys.argv[1]
	importimg(path)
