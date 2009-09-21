#!/usr/bin/env python
# encoding: utf-8
"""
exp1.py

First experiment: extremely simple region detection using thresholding.

Created by Oliver Smith on 2009-08-16.
Copyright (c) 2009 Oliver Smith. All rights reserved.
"""

import cv
import sys

val1 = 1

def chgv1(x):
	global val1
	val1 = x

def validate_contour(c):
	#x_min = min(pt[0] for pt in c)
	#x_max = max(pt[0] for pt in c)
	#y_min = min(pt[1] for pt in c)
	#y_max = max(pt[1] for pt in c)
	#dx = x_max - x_min
	#dy = y_max - y_min
	#d = dy!=0 and dx/dy or 0
	#return dx != 0 and dy != 0 and d>0.25 and d<4.0
	return cv.ContourArea(c) > 6

def main():
	global val1, val2
	img = cv.LoadImage(sys.argv[1])
	if img:
		cv.NamedWindow("bar")
		img2 = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U, 1)
		img21 = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U, 1)
		img3 = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_16S, 1)
		img4 = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U, 1)
		cv.CvtColor(img, img2, cv.CV_BGR2GRAY)
		cv.EqualizeHist(img2, img21)
		stor = cv.CreateMemStorage()
		cv.AdaptiveThreshold(img21, img4, 255, 
			cv.CV_ADAPTIVE_THRESH_GAUSSIAN_C, cv.CV_THRESH_BINARY_INV, 
			7, 7)
		cont = cv.FindContours(img4,
			stor,
			cv.CV_RETR_LIST,
			cv.CV_CHAIN_APPROX_NONE)
		img5 = cv.CloneImage(img)
		while cont:
			if validate_contour(cont):
				cv.DrawContours(img5, cont, (255,255,255), (255,255,255),0,2,8,(0,0))
			cont = cont.h_next()
		cv.ShowImage("bar", img5)
		cv.WaitKey(0)

if __name__ == '__main__':
	main()

