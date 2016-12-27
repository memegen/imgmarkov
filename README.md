# imgmarkov
Dreams up images using multi-dimensional markov chains.

![Screenshot 1](/screenshots/1.png?raw=true "Screenshot 1")
![Screenshot 2](/screenshots/2.png?raw=true "Screenshot 2")

## Dependencies
 - python 2
 - PIL
 - pypy (optional)

## Usage

**Step 1. import image** (try to keep dimensions below 200x200 pixels)
```
python import.py [<file>]
```
**Step 2. generate**
```
pypy imgmarkov.py [options]
options:
	--mode <n>	    Fill method 0 or 1.
	--copied <n>    Number of pixels to copy from original image.
	--silent        Turn off step-by-step graphical representation
```
**Step 3. export image**
```
python export.py [<path>]
```
