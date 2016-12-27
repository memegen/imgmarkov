"""
imgmarkov.py
Dreams up images using multi-dimensional markov chains

usage: pypy imgmarkov.py [options]
options:
	--mode <n>	    Fill method 0 or 1.
	--copied <n>    Number of pixels to copy from original image.
	--silent        Turn off step-by-step graphical representation

"""

import random
from Tkinter import *
import struct
import random
from sys import stdout
import sys

# initialization
lvl = 8
scale = 4
progress = 0
w = 0
h = 0
rawimg = []
img = []
genimg = []
chains = {}
nodes = []
master = Tk()
canvas = None


# loads the image data
def load_dat():
	global rawimg
	global img
	global w
	global h

	f1 = open("data/indat.txt").read()
	w = int(f1.split(";")[0].split("x")[0])
	h = int(f1.split(";")[0].split("x")[1])
	rawimg = f1.split(";")[1:]
	img = []

	for i in range(0,h):
		img.append([])
		for j in range(0,w):
			img[-1].append(",".join([str(int(n)//lvl) for n in rawimg[w*i+j].split(",")]))

	print "data loaded."


# returns a dictionary of direction vectors
def dirdict():
	#return {"-1,-1":{},"0,-1":{},"1,-1":{},"-1,0":{},"1,0":{},"-1,1":{},"0,1":{},"1,1":{}}
	d = {}
	for i in range(-1,2):
		for j in range(-1,2):
			if (i,j) != (0,0):
				d[str(i)+","+str(j)] = {}
	return d

# returns a list of direction vectors
def getdirs():
	return ["-1,-1","0,-1","1,-1","-1,0","1,0","-1,1","0,1","1,1"]
	#return dirdict().keys()


# generates a markov chain based on color information
def gen_chains():
	global chains
	chains = {}
	for i in range(0,h):
		for j in range(0,w):
			if not(img[i][j] in chains.keys()):
				chains[img[i][j]] = dirdict()


			for k in chains[img[i][j]].keys():
				dx = int(k.split(",")[0])
				dy = int(k.split(",")[1])
				if 0 <= j+dx < w and 0 <= i+dy < h:
					lc = img[i+dy][j+dx]
					if not(lc in chains[img[i][j]][k]):
						chains[img[i][j]][k][lc] = 0
					chains[img[i][j]][k][lc] += 1
						
	print "chain generated."

# extracts a random color from image
def randcol():
	try:
		return ",".join([str(int(int(n)//lvl)) for n in random.choice(rawimg[:-1]).split(",")])
	except:
		return "0,0,0"


# weighted random choice; 
# the chance of returning a key in the dict is proportional to its value
def wtchoice(dic):
	l = []
	for k in dic.keys():
		l.append([dic[k],k])
	for i in range(1,len(l)):
		l[i][0] = l[i][0]+l[i-1][0]
	t = l[-1][0]
	ri = random.uniform(0,t)
	for i in range(len(l)-1,0,-1):
		if ri > l[i-1][0]:
			return l[i][1]
	return l[0][1]

# merges a dict to another by addig to it its value multiplied by a factor
def adddict(d1,d2,mult=1):
	d3 = {}
	if d1:
		for k in d1.keys():
			d3[k] = d1[k]

	for k in d2.keys():
		if not(k in d3.keys()):
			d3[k] = 0
		d3[k] += d2[k]*mult
	return d3

# copies n random pixels from original image to generated image
def copyfixedpix(n):
	for r in range(0,n):
		ri = random.randrange(0,h)
		rj = random.randrange(0,w)
		genimg[ri][rj] = img[ri][rj]

# hex color to rgb color
def hex2rgb(rgb):
    return struct.unpack('BBB', rgb.decode('hex'))

# rgb color to hex color
def rgb2hex(rgb):
    return struct.pack('BBB',*rgb).encode('hex')

# paints a pixel according to the markov chain;
# then does a recursive flood fill
def flood(nd,silent=True):
	global nodes
	global progress
	global genimg
	global canvas
	i = nd[1]
	j = nd[0]
	pool = {randcol():1}
	for k in getdirs():
			dx = int(k.split(",")[0])
			dy = int(k.split(",")[1])
			if 0 <= j-dx < w and 0 <= i-dy < h and genimg[i-dy][j-dx] != None:
				for k1 in chains[genimg[i-dy][j-dx]].keys():
					pool = adddict(pool,chains[genimg[i-dy][j-dx]][k1],1.0/(dx**2+dy**2)**0.5)	
	col = wtchoice(pool)
	genimg[i][j] = col

	if not silent:
		rgbcol = tuple([int(c)* lvl for c in col.split(",")])
		canvas.create_rectangle(j*scale, i*scale, j*scale+scale, i*scale+scale, fill="#"+rgb2hex(rgbcol), width=0)

	nodes.remove(nd)
	progress += 1

	for k in ["0,-1","-1,0","1,0","0,1"]:
		dx = int(k.split(",")[0])
		dy = int(k.split(",")[1])
		if 0 <= j+dx < w and 0 <= i+dy < h and genimg[i+dy][j+dx] == None:
			if not [j+dx,i+dy] in nodes:
				nodes.append([j+dx,i+dy])

# inner main flow
def draw(mode=0,silent=True):
	global nodes
	global progress
	global genimg
	stdout.write("\r"+str(progress)+"/"+str(w*h)+" pixels generated...")
	stdout.flush()

	if mode == 0:
		for nd in nodes:
			flood(nd,silent)
	elif mode == 1:
		nd = random.choice(nodes)
		flood(nd,silent)

	if len(nodes)>0:
		canvas.after(1,draw,mode,silent)
	else:
		for i in range(0,h):
			for j in range(0,w):
				try:
					genimg[i][j] = [str(int(n)*lvl) for n in genimg[i][j].split(",")]
				except:
					genimg[i][j] = ['0','0','0']
		saveimg = str(w)+"x"+str(h)+";"
		for i in range(0,h):
			for j in range(0,w):
				saveimg += ",".join(genimg[i][j])+";"

		f2 = open("data/outdat.txt","w")
		f2.write(saveimg)
		print "\noutput saved."
		if silent:
			master.quit()

# generates a generative image
# mode: fill method
# copied: number of pixels to copy from original image
# silent: whether or not to render each step on tk canvas
def generate(mode = 0, copied = 0, silent = True):
	global genimg
	global progress
	global nodes
	global canvas

	load_dat()
	gen_chains()
	genimg = []
	for i in range(0,h):
		genimg.append([])
		for j in range(0,w):
			genimg[-1].append(None)

	nodes = [[random.randrange(0,w),random.randrange(0,h)],
			[random.randrange(0,w),random.randrange(0,h)]]

	copyfixedpix(copied)

	progress = len(nodes)

	if not silent:
		canvas = Canvas(master, width=w*scale, height=h*scale)
	else:
		canvas = Canvas(mater,0,0)
	canvas.pack()

	draw(mode=mode,silent=silent)
	


if __name__ == "__main__":
	mode = 0
	copied = 0
	silent = False
	try:
		arglist = sys.argv[1:]
		for i in range(0,len(arglist)):
			if arglist[i] == "--silent":
				silent = True
			elif arglist[i] == "--mode":
				mode = int(arglist[i+1])
			elif arglist[i] == "--copied":
				copied = int(arglist[i+1])
	except:
		"option(s) not recognized."

	generate(mode=mode,copied=copied,silent=silent)
	mainloop()

