#!/usr/bin/env python
# encoding: utf-8
"""
exputil.py

Common utility functions.

Created by Oliver Smith on 2009-08-31.
Copyright (c) 2009 Oliver Smith. All rights reserved.
"""

import cv

def quick_show(image):
	"""Display an image on the screen.
	
	Quick 'n' dirty method to throw up a window with an image in it and 
	wait for the user to dismiss it.
	"""
	cv.NamedWindow("foo")
	cv.ShowImage("foo", image)
	cv.WaitKey(0)
	cv.DestroyWindow("foo")

def max_contrast(image):
	"""Maximise the contrast on the image using top and bottom hat filters.
	"""
	size = cv.GetSize(image)
	bh = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
	th = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
	s1 = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
	s2 = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
	el = cv.CreateStructuringElementEx(3, 3, 1, 1, cv.CV_SHAPE_ELLIPSE)
	cv.MorphologyEx(image, th, None, el, cv.CV_MOP_TOPHAT, 1)
	cv.MorphologyEx(image, bh, None, el, cv.CV_MOP_BLACKHAT, 1)
	cv.Add(image, th, s1)
	cv.Sub(s1, bh, s2)
	return s2
		
def prepare_image(filename, invert=False):
	"""Prepare an image file for processing.

	Loads the file, converts the image to greyscale, enhances the contrast
	and (optionally) inverts it.
	"""
	ret = None
	image = cv.LoadImage(filename)
	size = cv.GetSize(image)
	if image:
		# convert to greyscale
		grey = extract_v(image)
		# maximise contrast
		eq_grey = max_contrast(grey)
		# (optionally) invert
		if invert:
			ret = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
			cv.XorS(eq_grey, 255, ret)
		else:
			ret = eq_grey
	return ret

def extract_v(image):
	size = cv.GetSize(image)
	hsv = cv.CreateImage(size, cv.IPL_DEPTH_8U, 3)
	v = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
	cv.CvtColor(image, hsv, cv.CV_RGB2HSV)
	cv.SetImageCOI(hsv, 3)
	cv.Copy(hsv, v)
	return v

def greyscale(image):
	grey = cv.CreateImage((image.width,image.height), cv.IPL_DEPTH_8U, 1)
	cv.CvtColor(image, grey, cv.CV_BGR2GRAY)
	return grey

