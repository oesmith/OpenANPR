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
import math

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
	# load image
	orig = cv.LoadImage(args[0])
	size = (orig.width, orig.height)
	# convert to greyscale
	grey = extract_v(orig)
	# invert, if required
	if invert:
		inv = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
		cv.XorS(grey, 255, inv)
		grey = inv
	grey = max_contrast(cv.CloneImage(grey))
	# a bit of smoothing to reduce noise
	smoothed = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
	cv.Smooth(grey, smoothed, cv.CV_GAUSSIAN, 3, 3)
	# adaptive thresholding finds the letters against the numberplate
	# background
	image2 = cv.CloneImage(grey)
	cv.AdaptiveThreshold(smoothed, image2, 255, 
		cv.CV_ADAPTIVE_THRESH_GAUSSIAN_C, cv.CV_THRESH_BINARY_INV, 
		7, 7)
	# use a hough transform to find straight edges in the image and then 
	# remove them - removes number plate edges to ensure that characters 
	# don't join with the edges of the plate
	storage = cv.CreateMemStorage()
	lines = cv.HoughLines2(image2, storage, cv.CV_HOUGH_PROBABILISTIC,
	                       1, math.pi/180, 50, 35, 2);
	for line in lines:
		cv.Line( image2, line[0], line[1], 0, 2, 8 );
	quick_show(image2)
	
	# TODO: tweak this lot to remove noisy little blobs from the image
	#
	#con = connected(image2)
	#quick_show(con)
	#el = cv.CreateStructuringElementEx(1,3,0,1,cv.CV_SHAPE_RECT)
	#el2 = cv.CreateStructuringElementEx(3,1,1,0,cv.CV_SHAPE_RECT)
	#el3 = cv.CreateStructuringElementEx(7,3,3,1,cv.CV_SHAPE_RECT)
	#morph = cv.CloneImage(grey)
	#cv.Erode(image2, morph, el, iterations=2)
	#quick_show(morph)
	#morph2 = cv.CloneImage(grey)
	#cv.Dilate(morph, morph2, iterations=10)
	#quick_show(morph2)
	#quick_show(connected(morph2))
	#foo = cv.CreateImage(size, cv.IPL_DEPTH_8U, 3)
	#cv.Copy(orig, foo, image2)
	#quick_show(foo)
	#quick_show(connected(foo))


if __name__ == '__main__':
	main()

