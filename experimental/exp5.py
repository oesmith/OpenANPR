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
from getopt import getopt
import math

import cv

from exputil import *
from connected import *

def syntax():
	"""Print the command line syntax."""
	msgs = [
		"Syntax: exp4.py [-i] imagefile",
		"Options:",
		"     -i  Invert the image (select dark objects)"]
	print "\n".join(msgs)

def validate_contour(c):
	x_min = min(pt[0] for pt in c)
	x_max = max(pt[0] for pt in c)
	y_min = min(pt[1] for pt in c)
	y_max = max(pt[1] for pt in c)
	dx = x_max - x_min + 1
	dy = y_max - y_min + 1
	d = float(dx)/float(dy)
	a = dx*dy
	i = float(len(c))/a
	g = 0.3
	if (len(c)>8 and a>20 and dy>10 and dy<50 and dx<50 and 
			d>0.125 and d<8 and i>0.02):
		return (x_min-dx*g, y_min-dy*g, x_max+dx*g, y_max+dy*g)
	else:
		return None

def overlaps(a, b):
	# return true if two bboxes overlap
	if id(a) == id(b):
		return False
	else:
		day = a[3] - a[1]
		dax = a[2] - a[0]
		dby = b[3] - b[1]
		dbx = b[2] - b[0]
		return(a[0] <= b[2] and a[1] <= b[3] and 
		       a[2] > b[0] and a[3] > b[1] and 
		       (day >= dby*.9 and day <= dby*1.1 or
		       dax >= dbx*.9 and dax <= dbx*1.1) )

def find_overlap(candidate, bboxes):
	# return true if bbox candidate overlaps another bbox in list bboxes
	for bbox in bboxes:
		if overlaps(candidate, bbox):
			return True
	return False

def main():
	"""Parse the command line and set off processing."""
	# parse command line
	opts,args = getopt(sys.argv[1:], "i")
	if len(args) != 1:
		syntax()
		return 1
	# grab options
	invert = False
	for n,v in opts:
		if n == '-i':
			invert = True
	# load image
	grey = prepare_image(args[0], invert)
	size = cv.GetSize(grey)
	# a bit of smoothing to reduce noise
	smoothed = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
	cv.Smooth(grey, smoothed, cv.CV_GAUSSIAN, 5, 5)
	# adaptive thresholding finds the letters against the numberplate
	# background
	thresholded = cv.CloneImage(grey)
	cv.AdaptiveThreshold(smoothed, thresholded, 255, 
		cv.CV_ADAPTIVE_THRESH_GAUSSIAN_C, cv.CV_THRESH_BINARY_INV, 
		19, 9)
	# use a hough transform to find straight edges in the image and then 
	# remove them - removes number plate edges to ensure that characters 
	# don't join with the edges of the plate
	storage = cv.CreateMemStorage()
	lines = cv.HoughLines2(thresholded, storage, cv.CV_HOUGH_PROBABILISTIC,
	                       1, math.pi/180, 50, 50, 2)
	for line in lines:
		cv.Line(thresholded, line[0], line[1], 0, 3, 4)
	#quick_show(th)
	#return
	# grab the contours from the image
	cont = cv.FindContours(thresholded,
		storage,
		cv.CV_RETR_CCOMP,
		cv.CV_CHAIN_APPROX_NONE)
	# grab 'good' contours
	col = 128
	validated = []
	while cont:
		v = validate_contour(cont)
		if v is not None:
			validated.append(v)
		cont = cont.h_next()
	overlapping = []
	for v in validated:
		if find_overlap(v, validated):
			overlapping.append(v)
	# overlay bounding boxes of 'good' contours on the original image
	print len(overlapping)
	result = cv.LoadImage(args[0])
	for bbox in overlapping:
		cv.Rectangle(result, (int(bbox[0]),int(bbox[1])), 
			(int(bbox[2]), int(bbox[3])), (255,0,0))
	quick_show(result)


if __name__ == '__main__':
	main()

