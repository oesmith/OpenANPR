#!/usr/bin/env python
# encoding: utf-8
"""
exp6.py

An attempt to reproduce this research:
http://ecet.ecs.ru.acad.bg/cst04/Docs/sIIIA/32.pdf

Created by Oliver Smith on 2009-09-04.
Copyright (c) 2009 Oliver Smith. All rights reserved.
"""

import sys
import os

import cv

from exputil import *

W = 320

def main():
	# load the specified image
	filename = sys.argv[1]
	original = cv.LoadImage(filename)
	# resample to W columns wide
	aspect = float(original.width) / float(original.height)
	print original.width, original.height
	print W, int(W/aspect)
	resized = cv.CreateImage((W, int(W/aspect)), cv.IPL_DEPTH_8U, 3)
	cv.Resize(original, resized, cv.CV_INTER_NN)
	quick_show(resized)
	resized = extract_v(resized)
	for y in range(resized.height-1):
		for x in range(resized.width-1):
			p1 = resized[y,x]
			p2 = resized[y,x+1]
			p3 = resized[y+1,x]
			p4 = resized[y+1,x+1]
			resized[y,x] = abs(p1-p4) + abs(p2-p3)
	mean = cv.CreateImage((resized.width,resized.height), cv.IPL_DEPTH_8U, 1)
	for y in range(1,resized.height-3):
		for x in range(1,resized.width-3):
			a = 0.0
			for yy in range(y-1,y+3):
				for xx in range(x-1,x+3):
					a += resized[yy,xx]
			mean[y,x] = a/16.0
	gray = cv.CreateImage((original.width,original.height), cv.IPL_DEPTH_8U, 1)
	cv.Resize(mean, gray)
	quick_show(gray)


if __name__ == '__main__':
	main()

