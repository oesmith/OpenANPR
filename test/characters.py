#!/usr/bin/env python
# encoding: utf-8
"""
test/characters.py

Testing character extraction.

Created by Oliver Smith on 2009-09-26.
Copyright (c) 2009 Oliver Smith. All rights reserved.
"""

import os
import cv
import anpr
from quick_show import quick_show

files = os.listdir('data/examples')
counter = 0
for f in files:
	image = cv.LoadImage('data/examples/'+f)
	for plate in anpr.detect_plates(image):
		zzz = cv.CreateImage(cv.GetSize(plate), cv.IPL_DEPTH_8U, 3)
		cv.Smooth(plate, zzz)
		#
		cv.PyrMeanShiftFiltering(plate, zzz, 40, 15)
		foo = anpr.greyscale(plate)
		segmented = cv.CreateImage(cv.GetSize(plate), cv.IPL_DEPTH_8U, 1)
		bar = cv.CreateImage(cv.GetSize(plate), cv.IPL_DEPTH_8U, 1)
		cv.EqualizeHist(foo, segmented)
		cv.AdaptiveThreshold(segmented, bar, 255, 
			cv.CV_ADAPTIVE_THRESH_GAUSSIAN_C, cv.CV_THRESH_BINARY_INV,
			plate.height%2 == 0 and (plate.height+1) or plate.height, 
			plate.height/2)
		baz = cv.CreateImage(cv.GetSize(plate), cv.IPL_DEPTH_8U, 1)
		el = cv.CreateStructuringElementEx(1, 2, 0, 0, cv.CV_SHAPE_RECT)
		cv.Erode(bar, baz, el)
		for char in anpr.find_characters(foo, baz):
			cv.Rectangle(plate, (int(char.x1),int(char.y1)), 
				(int(char.x2), int(char.y2)), (255,0,0))
		quick_show(plate)
