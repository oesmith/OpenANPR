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
for f in files:
    image = cv.LoadImage('data/examples/'+f)
    for plate in anpr.detect_plates(image):
        plate_grey = anpr.greyscale(plate)
        hist = cv.CreateHist([256], cv.CV_HIST_ARRAY, [[0,255]])
        cv.CalcHist([plate_grey], hist)
        total_pixels = plate_grey.width * plate_grey.height
        accum = 0
        threshold = 0
        for i in range(0,256):
            accum += cv.QueryHistValue_1D(hist, i)
            if accum > total_pixels*.45:
                threshold = i
                break
        print threshold
        plate_mono = cv.CreateImage((plate.width,plate.height), 
                                    cv.IPL_DEPTH_8U, 
                                    1)
        cv.Threshold(plate_grey, 
                     plate_mono, 
                     threshold, 
                     255.0, 
                     cv.CV_THRESH_BINARY)
        for x in range(0, plate.width):
            c = 0
            for y in range(0, plate.height):
                if cv.Get2D(plate_mono, y, x)[0]:
                    c += 1
            print "=" * c
        cv.SaveImage('output%02d.png' % counter, plate_mono)
        counter = counter+1

