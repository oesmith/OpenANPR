#!/usr/bin/env python
# encoding: utf-8
"""
anpr/preprocess.py

Image pre-processing for character detection.

Created by Oliver Smith on 2009-09-26.
Copyright (c) 2009 Oliver Smith. All rights reserved.
"""

import cv

SMOOTH_FILTER_SIZE = 5
ADAPTIVE_THRESH_BLOCK_SIZE = 19
ADAPTIVE_THRESH_WEIGHT = 9

def preprocess(image, otsu_thresh=False):
	"""Pre-process an image ready for character contour detection."""
	size = cv.GetSize(image)
	# convert to single channel
	grey = extract_v(image)
	# maximise contrast
	max_grey = max_contrast(grey)
	# a bit of smoothing to reduce noise
	smoothed = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
	cv.Smooth(max_grey, smoothed, cv.CV_GAUSSIAN, SMOOTH_FILTER_SIZE)
	# adaptive thresholding finds the letters against the numberplate
	# background
	thresholded = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
	if otsu_thresh:
		cv.Threshold(smoothed, thresholded, 0, 255, 
			cv.CV_THRESH_BINARY_INV | cv.CV_THRESH_OTSU)
	else:
		cv.AdaptiveThreshold(smoothed, thresholded, 255, 
			cv.CV_ADAPTIVE_THRESH_GAUSSIAN_C, cv.CV_THRESH_BINARY_INV, 
			ADAPTIVE_THRESH_BLOCK_SIZE, ADAPTIVE_THRESH_WEIGHT)
	return grey, thresholded


def max_contrast(image):
	"""Maximise the contrast of an image using top and bottom hat filters."""
	size = cv.GetSize(image)
	bh = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
	th = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
	s1 = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
	s2 = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
	el = cv.CreateStructuringElementEx(3, 3, 1, 1, cv.CV_SHAPE_ELLIPSE)
	cv.MorphologyEx(image, th, None, el, cv.CV_MOP_TOPHAT, 1)
	cv.MorphologyEx(image, bh, None, el, cv.CV_MOP_BLACKHAT, 1)
	cv.Add(image, th, s1)
	cv.Sub(s1, bh, s2)
	return s2


def extract_v(image):
	"""Convert an RGB image to HSV and extract the V component.	"""
	size = cv.GetSize(image)
	hsv = cv.CreateImage(size, cv.IPL_DEPTH_8U, 3)
	v = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
	cv.CvtColor(image, hsv, cv.CV_RGB2HSV)
	cv.SetImageCOI(hsv, 3)
	cv.Copy(hsv, v)
	return v

def greyscale(image):
	grey = cv.CreateImage((image.width,image.height), cv.IPL_DEPTH_8U, 1)
	cv.CvtColor(image, grey, cv.CV_RGB2GRAY)
	return grey
		