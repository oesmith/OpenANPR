#!/usr/bin/env python
# encoding: utf-8
"""
test/quick_show.py

Quick 'n' dirty image display.

Created by Oliver Smith on 2009-09-26.
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
