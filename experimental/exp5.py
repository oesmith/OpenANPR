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

class Box(object):
	def __init__(self, image, x1, y1, x2, y2):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.w = self.x2 - self.x1
		self.h = self.y2 - self.y1
		self.a = self.w / self.h
		self.cx = (self.x1 + self.x2) / 2
		self.cy = (self.y1 + self.y2) / 2
		cv.SetImageROI(image, (self.x1, self.y1, self.w, self.h))
		#self.hist = cv.CreateHist ([16], cv.CV_HIST_ARRAY, [[0,256]])
		#cv.CalcHist([image], self.hist, 0)
		#cv.NormalizeHist(self.hist, 100)
		self.avg,self.sdv = cv.AvgSdv(image)
		self.avg = self.avg[0]
		self.sdv = self.sdv[0]
		cv.ResetImageROI(image)
	
	def overlaps(self, o):
		return( id(self) != id(o) and
		        self.x1 <= o.x2 and self.y1 <= o.y2 and 
		        self.x2 > o.x1 and self.y2 > o.y1 )
	
	def dist_to(self, o):
		x = self.cx - o.cx
		y = self.cy - o.cy
		return math.sqrt(x*x + y*y)
	
	def similar_to(self, o):
		return (abs(self.w-o.w) < 8 and
			abs(self.h-o.h) < 8 and 
			(self.avg-o.avg)/self.avg < 0.3 and
			(self.sdv-o.sdv)/self.sdv < 0.3)

def syntax():
	"""Print the command line syntax."""
	msgs = [
		"Syntax: exp4.py [-i] imagefile",
		"Options:",
		"     -i  Invert the image (select dark objects)"]
	print "\n".join(msgs)

def validate_contour(c,image):
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
	if (len(c)>8 and a>20 and dy>8 and dy<50 and dx<50 and 
			d>0.125 and d<8 and i>0.02):
		return Box(image, x_min, y_min, x_max, y_max)
	else:
		return None

def find_overlap(candidate, bboxes):
	# return true if bbox candidate overlaps another bbox in list bboxes
	for bbox in bboxes:
		if overlaps(candidate, bbox):
			return True
	return False
	

def fit_line(line, first, second):
	x1, y1 = line[0:2]
	d = first.dist_to(second)
	x2 = (second.cx - first.cx)/d
	y2 = (second.cy - first.cy)/d
	dp = x1*x2 + y1*y2
	a = math.acos(dp)
	if abs(a) > math.pi/2.0:
		a = math.pi - abs(a)
	return a < math.pi/40.0

def cluster_fuck(bboxes):
	clusters = []
	for i in bboxes:
		line = None
		cluster = set((i,))
		nb = [(b, i.dist_to(b)) for b in bboxes if b != i and i.similar_to(b)]
		nb.sort(cmp=lambda x,y: cmp(x[1],y[1]))
		for b,d in nb:
			dists = [j.dist_to(b) for j in cluster]
			if min(dists) < math.sqrt(b.w*b.w+b.h*b.h)*1.6:
				if line is None or fit_line(line, i, b):
					cluster.add(b)
					d = i.dist_to(b)
					if line is None and d != 0.0:
						line = ((b.cx-i.cx)/d, (b.cy-i.cy)/d)
		if len(cluster)>3:
			# TODO: line fitting?
			clusters.append(cluster)
	clusters.sort(cmp=lambda x,y: cmp(len(x),len(y)))
	if len(clusters):
		return [clusters[-1]] + cluster_fuck(bboxes.difference(clusters[-1]))
	else:
		return []
	
	
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
	#lines = cv.HoughLines2(thresholded, storage, cv.CV_HOUGH_PROBABILISTIC,
	#                       1, math.pi/180, 50, 50, 2)
	#for line in lines:
	#	cv.Line(thresholded, line[0], line[1], 0, 3, 4)
	# grab the contours from the image
	cont = cv.FindContours(thresholded,
		storage,
		cv.CV_RETR_CCOMP,
		cv.CV_CHAIN_APPROX_NONE)
	# grab 'good' contours
	col = 128
	validated = []
	while cont:
		v = validate_contour(cont,grey)
		if v is not None:
			validated.append(v)
		cont = cont.h_next()
	# overlay bounding boxes of 'good' contours on the original image
	result = cv.LoadImage(args[0])
	clusters = cluster_fuck(set(validated))
	for cluster in clusters:
		cv.Rectangle(result, 
			(int(min([c.x1 for c in cluster])), 
			 int(min([c.y1 for c in cluster]))),
			(int(max([c.x2 for c in cluster])), 
			 int(max([c.y2 for c in cluster]))), 
			(0,0,255))
		for bbox in cluster:
			cv.Rectangle(result, (int(bbox.x1),int(bbox.y1)), 
				(int(bbox.x2), int(bbox.y2)), (255,0,0))
	quick_show(result)


if __name__ == '__main__':
	main()

