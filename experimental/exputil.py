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
		grey = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
		cv.CvtColor(image, grey, cv.CV_BGR2GRAY)
		# maximise contrast
		eq_grey = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
		cv.EqualizeHist(grey, eq_grey)
		# (optionally) invert
		if invert:
			ret = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
			cv.XorS(eq_grey, 255, ret)
		else:
			ret = eq_grey
	return ret

