#!/usr/bin/env python
# encoding: utf-8
"""
test/contour.py

Testing cluster processing.

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
	for cluster in anpr.find_clusters(contours):
		cv.Rectangle(image, 
			(int(min([c.x1 for c in cluster])), 
			 int(min([c.y1 for c in cluster]))),
			(int(max([c.x2 for c in cluster])), 
			 int(max([c.y2 for c in cluster]))), 
			(0,0,255))
		for bbox in cluster:
			cv.Rectangle(image, (int(bbox.x1),int(bbox.y1)), 
				(int(bbox.x2), int(bbox.y2)), (255,0,0))
	quick_show(image)