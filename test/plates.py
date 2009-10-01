
#!/usr/bin/env python
# encoding: utf-8
"""
test/plates.py

Testing plate detection.

Created by Oliver Smith on 2009-09-26.
Copyright (c) 2009 Oliver Smith. All rights reserved.
"""

import os
import cv
import anpr
from quick_show import quick_show

files = os.listdir('data/examples')
counter = 0
for f in ['30082009_007.jpg']:
	image = cv.LoadImage('data/examples/'+f)
	for plate in anpr.detect_plates(image):
		cv.SaveImage('output%02d.png' % counter, plate)
		counter = counter+1