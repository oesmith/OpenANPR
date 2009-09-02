#!/usr/bin/env python
# encoding: utf-8
"""
exp5.py

Experiment 5: playing with the 'other' OpenCV API.

Created by Oliver Smith on 2009-08-31.
Copyright (c) 2009 Oliver Smith. All rights reserved.
"""

import sys
import os
from getopt import getopt

import cv

from exputil import *
from connected import *

def syntax():
	"""Print the command line syntax."""
	msgs = [
		"Syntax: exp4.py [-i] imagefile",
		"Options:",
		"     -i  Invert the image (select dark objects)"]
	print "\n".join(msgs)

def main():
	"""Parse the command line and set off processing."""
	# parse command line
	opts,args = getopt(sys.argv[1:], "i")
	if len(args) != 1:
		syntax()
		return 1
	# grab options
	invert = False
	for n,v in opts:
		if n == '-i':
			invert = True
	# prepare image
	orig = cv.LoadImage(args[0])
	size = (orig.width, orig.height)
	grey = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
	cv.CvtColor(orig, grey, cv.CV_BGR2GRAY)
	if invert:
		inv = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
		cv.XorS(grey, 255, inv)
		grey = inv
	smoothed = max_contrast(cv.CloneImage(grey))
	cv.Smooth(grey, smoothed)
	image2 = cv.CloneImage(grey)
	cv.AdaptiveThreshold(smoothed, image2, 255, 
		cv.CV_ADAPTIVE_THRESH_GAUSSIAN_C, cv.CV_THRESH_BINARY_INV, 
		7, 5)
	quick_show(image2)
	#el = cv.CreateStructuringElementEx(3,3,1,1,cv.CV_SHAPE_RECT)
	#morph = cv.CloneImage(grey)
	#cv.MorphologyEx(image2, morph, None, el, cv.CV_MOP_OPEN, 1)
	#quick_show(morph)
	#morph2 = cv.CloneImage(grey)
	#cv.MorphologyEx(morph, morph2, None, el, cv.CV_MOP_CLOSE, 3)
	#quick_show(morph2)
	#foo = cv.CloneImage(grey)
	#cv.Sub(image2, morph, foo)
	quick_show(connected(image2))


if __name__ == '__main__':
	main()

