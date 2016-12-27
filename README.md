# imgmarkov
Dreams up images using multi-dimensional markov chains.

# Dependencies
 - python 2
 - PIL
 - pypy (optional)

# Usage

## Step 1. import
```
python import.py [<file>]
```
## Step 2. generate 
```
pypy imgmarkov.py [options]
options:
	--mode <n>	    Fill method 0 or 1.
	--copied <n>    Number of pixels to copy from original image.
	--silent        Turn off step-by-step graphical representation
```
## Step 3. export
```
python export.py [<path>]
```
