#!/usr/bin/env python
# encoding: utf-8
"""
anpr/detect.py

Number plate region detection/extraction.

Created by Oliver Smith on 2009-09-26.
Copyright (c) 2009 Oliver Smith. All rights reserved.
"""

import cv

from preprocess import *
from contour import *


def detect_plates(image):
	"""Detects possible number plate regions in an image."""
	grey, bw = preprocess(image)
	contours = set(find_characters(grey, bw))
	for cluster in find_clusters(contours):
		plate = extract_plate(image, cluster)
		if plate is not None:
			yield plate


def find_characters(grey, bw):
	"""Find character contours in a 1-bit image."""
	# detect contours
	storage = cv.CreateMemStorage()
	contour_iter = cv.FindContours(bw,
		storage,
		cv.CV_RETR_CCOMP,
		cv.CV_CHAIN_APPROX_NONE)
	# filter the detected contours
	while contour_iter:
		contour = Contour(contour_iter, grey)
		if contour.valid:
			yield contour
		contour_iter = contour_iter.h_next()


def extract_plate(image, cluster):
	"""De-skew and extract a detected plate from an image."""
	cluster = list(cluster)
	cluster.sort(cmp=lambda x,y: cmp(x.cx,y.cx))
	o = cluster[-1].cy - cluster[0].cy
	h = cluster[0].dist_to(cluster[-1])
	angle = math.asin(o/h)
	matrix = cv.CreateMat(2, 3, cv.CV_32FC1)
	cx = (cluster[0].cx + cluster[-1].cx)/2.0
	cy = (cluster[0].cy + cluster[-1].cy)/2.0
	cv.GetRotationMatrix2D((cx,cy), angle*180.0/math.pi, 1, matrix)
	warp = cv.CreateImage(cv.GetSize(image), 
		cv.IPL_DEPTH_8U, 3)
	cv.WarpAffine(image, warp, matrix)
	ret = cv.CreateImage((int(h+cluster[0].dia*3.0), int(cluster[0].dia*1.5)), 
	    cv.IPL_DEPTH_8U, 3)
	cv.GetRectSubPix(warp, ret, (cx,cy))
	print cv.GetSize(ret)
	return ret