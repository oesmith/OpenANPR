#!/usr/bin/env python
# encoding: utf-8
"""
exp4.py

Experiment 4: playing around with brightness/contrast enhancement.

Created by Oliver Smith on 2009-08-21.
Copyright (c) 2009 Oliver Smith. All rights reserved.
"""

from getopt import getopt
import sys

from opencv.cv import *
from opencv.highgui import *

def quick_show(image):
	"""Display an image on the screen.
	
	Quick 'n' dirty method to throw up a window with an image in it and 
	wait for the user to dismiss it.
	"""
	cvNamedWindow("bar")
	cvShowImage("bar", image)
	cvWaitKey(0)
	cvDestroyWindow("bar")

def max_contrast(image):
	"""Maximise the contrast on the image using top and bottom hat filters.
	"""
	size = cvGetSize(image)
	bh = cvCreateImage(size, IPL_DEPTH_8U, 1)
	th = cvCreateImage(size, IPL_DEPTH_8U, 1)
	s1 = cvCreateImage(size, IPL_DEPTH_8U, 1)
	s2 = cvCreateImage(size, IPL_DEPTH_8U, 1)
	el = cvCreateStructuringElementEx(3, 3, 2, 2, CV_SHAPE_ELLIPSE)
	cvMorphologyEx(image, th, None, el, CV_MOP_TOPHAT, 1)
	cvMorphologyEx(image, bh, None, el, CV_MOP_BLACKHAT, 1)
	cvAdd(image, th, s1)
	cvSub(s1, bh, s2)
	return s2

def generate_tree(image):
	"""Generate the component tree.
	
	Incrementally threshold the image, doing connected component analysis 
	at each level and building up a tree of related components at each 
	threshold level.
	"""
	size = cvGetSize(image)
	for level in range(1,255):
		# TODO
		pass

def prepare_image(filename, invert=False):
	"""Prepare an image file for processing.
	
	Loads the file, converts the image to greyscale, enhances the contrast
	and (optionally) inverts it.
	"""
	ret = None
	image = cvLoadImage(filename)
	size = cvGetSize(image)
	if image:
		# convert to greyscale
		grey = cvCreateImage(size, IPL_DEPTH_8U, 1)
		cvCvtColor(image, grey, CV_BGR2GRAY)
		cvReleaseImage(image)
		# maximise contrast
		eq_grey = cvCreateImage(size, IPL_DEPTH_8U, 1)
		cvEqualizeHist(grey, eq_grey)
		cvReleaseImage(grey)
		# (optionally) invert
		if invert:
			ret = cvCreateImage(size, IPL_DEPTH_8U, 1)
			cvXorS(eq_grey, cvScalar(255), ret)
			cvReleaseImage(eq_grey)
		else:
			ret = eq_grey
	return ret

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
	image = prepare_image(args[0], invert)
	
	quick_show(image)
	quick_show(max_contrast(image))

if __name__ == '__main__':
	main()

