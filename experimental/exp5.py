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

import cv

from exputil import *
from connected import *

def main():
	"""Main entry point."""
	image1 = prepare_image(sys.argv[1], True)
	image = cv.CloneImage(image1)
	cv.Smooth(image1,image)
	quick_show(image)
	image2 = cv.CreateImage((image.width,image.height), cv.IPL_DEPTH_8U, 1)
	cv.Threshold(image, image2, 150, 255, cv.CV_THRESH_BINARY)
	quick_show(connected(image2))


if __name__ == '__main__':
	main()

