"""
export.py
Renders an image from output data of imgmarkov.py

usage: python export.py [<path>]

"""


from PIL import Image, ImageDraw
import sys
import time

# initialization
im = None
dr = None

# renders an image from output data
def imgfrom(outdat):
	global im
	global dr

	f1 = open(outdat,'r').read()

	scale = 4
	w,h = f1.split(";")[0].split("x")
	w,h = int(w),int(h)
	pixseq = f1.split(";")[1:]

	im = Image.new("RGB",(w*scale,h*scale))

	dr = ImageDraw.Draw(im)


	for i in range(0,h):
		for j in range(0,w):
			col = tuple([int(n) for n in pixseq[w*i+j].split(",")])
			dr.rectangle([j*scale,i*scale,(j+1)*scale,(i+1)*scale],fill=col)
	del dr
	
# display the image using default show method
def showimg(): im.show()


if __name__ == "__main__":
	imgfrom("data/outdat.txt")
	
	outpath = "generated/output"+str(time.time())+".jpg"
	if len(sys.argv) > 1:
		outpath = sys.argv[1]
	fo = open(outpath,"w")
	im.save(fo)
	print "saved to "+outpath+"."
	showimg()