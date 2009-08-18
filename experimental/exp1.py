#!/usr/bin/env python
# encoding: utf-8
"""
exp1.py

First experiment: extremely simple region detection using thresholding.

Created by Oliver Smith on 2009-08-16.
Copyright (c) 2009 Oliver Smith. All rights reserved.
"""

from opencv.cv import *
from opencv.highgui import *
import sys

val1 = 1

def chgv1(x):
	global val1
	val1 = x

def validate_contour(c):
	x_min = min(pt.x for pt in c)
	x_max = max(pt.x for pt in c)
	y_min = min(pt.y for pt in c)
	y_max = max(pt.y for pt in c)
	dx = x_max - x_min
	dy = y_max - y_min
	d = dy!=0 and dx/dy or 0
	return dx != 0 and dy != 0 and d>0.25 and d<4.0

def main():
	global val1, val2
	img = cvLoadImage(sys.argv[1])
	if img:
		cvNamedWindow("bar")
		cvCreateTrackbar("tb1", "bar", val1, 255, chgv1)
		img2 = cvCreateImage(cvGetSize(img), IPL_DEPTH_8U, 1)
		img21 = cvCreateImage(cvGetSize(img), IPL_DEPTH_8U, 1)
		img3 = cvCreateImage(cvGetSize(img), IPL_DEPTH_16S, 1)
		img4 = cvCreateImage(cvGetSize(img), IPL_DEPTH_8U, 1)
		cvCvtColor(img, img2, CV_BGR2GRAY)
		cvEqualizeHist(img2, img2)
		cvSmooth(img2, img21)
		stor = cvCreateMemStorage(0)
		while cvWaitKey(15) != chr(27):
			cvThreshold(img21, img4, val1, 255, CV_THRESH_BINARY)
			nb_contours, cont = cvFindContours(img4,
				stor,
				sizeof_CvContour,
				CV_RETR_LIST,
				CV_CHAIN_APPROX_NONE,
				cvPoint (0,0))
			img5 = cvClone(img)
			for c in cont.hrange():
				if validate_contour(c):
					cvDrawContours(img5, c, CV_RGB(255,255,255), CV_RGB(255,255,255),0,2,8,cvPoint(0,0))
			cvShowImage("bar", img5)

if __name__ == '__main__':
	main()

