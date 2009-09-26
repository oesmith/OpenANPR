#!/usr/bin/env python
# encoding: utf-8
"""
test/contour.py

Testing contour processing.

Created by Oliver Smith on 2009-09-26.
Copyright (c) 2009 Oliver Smith. All rights reserved.
"""

import os
import cv
import anpr
from quick_show import quick_show

files = os.listdir('data/examples')
for f in files:
	image = cv.LoadImage('data/examples/'+f)
	grey,bw = anpr.preprocess(image)
	contours = set(anpr.find_characters(grey, bw))
	for bbox in contours:
		cv.Rectangle(image, (int(bbox.x1),int(bbox.y1)), 
			(int(bbox.x2), int(bbox.y2)), (255,0,0))
	quick_show(image)