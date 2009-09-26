#!/usr/bin/env python
# encoding: utf-8
"""
anpr/contour.py

Contour processing/filtering/clustering.

Created by Oliver Smith on 2009-09-26.
Copyright (c) 2009 Oliver Smith. All rights reserved.
"""

import math
import cv

MAX_CLUSTER_GRADIENT_DIFF = 0.1
MAX_CLUSTER_DIST_FACTOR = 1.5
MIN_CLUSTER_SIZE = 3

def find_clusters(contours):
	ret = []
	# iterate over the set of contours, attempting to find the candidate
	# that produces the largest cluster
	for candidate in contours:
		# line to fit the cluster to
		gradient = None
		# the cluster
		cluster = set((candidate,))
		# make a list of contours that are similar to the candidate, then
		# sort them by distance from the candidate
		sorted_similar_contours = list(candidate.potential_matches(contours))
		sorted_similar_contours.sort(cmp=lambda x,y: cmp(x[1], y[1]))
		# iterate over each contour in the sorted list
		for other, distance in sorted_similar_contours:
			# find the distance to the closest member of the cluster
			dists = [c.dist_to(other) for c in cluster]
			if min(dists) < other.dia*MAX_CLUSTER_DIST_FACTOR:
				other_gradient = candidate.gradient_to(other)
				if gradient is None or abs(gradient-other_gradient) < MAX_CLUSTER_GRADIENT_DIFF:
					cluster.add(other)
					if gradient is None:
						gradient = other_gradient
		if len(cluster)>=MIN_CLUSTER_SIZE:
			ret.append(cluster)
	ret.sort(cmp=lambda x,y: cmp(len(x), len(y)))
	if len(ret):
		best = ret[-1]
		return [best] + find_clusters(contours.difference(best))
	else:
		return []


class Contour(object):
	# contour filter criteria
	MIN_PIXELS = 8
	MIN_WIDTH = 2
	MIN_HEIGHT = 8
	MAX_WIDTH = 50
	MAX_HEIGHT = 50
	MIN_ASPECT = 0.1
	MAX_ASPECT = 3.0
	MIN_AREA = 20
	MIN_DENSITY = 0.01
	# similarity criteria
	MAX_HEIGHT_DIFF = 8
	MAX_WIDTH_DIFF = 8
	MAX_AVG_FACTOR = 0.2
	MAX_SDV_FACTOR = 0.2
	# match criteria
	MIN_DIST_FACTOR = 0.3
	MAX_DIST_FACTOR = 10.0
	MAX_ANGLE = math.pi/4
	
	def __init__(self, contour, image):
		self.valid = False
		# save the contour
		self.contour = contour
		if len(contour)<Contour.MIN_PIXELS:
			return
		# left, top, right, bottom
		self.x1 = min(pt[0] for pt in contour)
		self.y1 = min(pt[1] for pt in contour)
		self.x2 = max(pt[0] for pt in contour)
		self.y2 = max(pt[1] for pt in contour)
		# width/height
		self.width = self.x2 - self.x1
		self.height = self.y2 - self.y1
		if self.width<Contour.MIN_WIDTH or self.width>Contour.MAX_WIDTH:
			return
		if self.height<Contour.MIN_HEIGHT or self.height>Contour.MAX_HEIGHT:
			return
		# centre
		self.cx = (self.x1 + self.x2)/2
		self.cy = (self.y1 + self.y2)/2
		# diagonal size
		self.dia = math.sqrt(self.width*self.width + self.height*self.height)
		# aspect
		self.aspect = float(self.width)/float(self.height)
		if self.aspect<Contour.MIN_ASPECT or self.aspect>Contour.MAX_ASPECT:
			return
		# area
		self.area = self.width * self.height
		if self.area<Contour.MIN_AREA:
			return
		# density
		self.density = len(contour)/float(self.area)
		if self.density<Contour.MIN_DENSITY:
			return
		cv.SetImageROI(image, (self.x1, self.y1, self.width, self.height))
		self.avg,self.sdv = cv.AvgSdv(image)
		self.avg = self.avg[0]
		self.sdv = self.sdv[0]
		cv.ResetImageROI(image)
		# done!
		self.valid = True
	
	def dist_to(self, other):
		x = self.cx - other.cx
		y = self.cy - other.cy
		return math.sqrt(x*x + y*y)
	
	def gradient_to(self,other):
		p1,p2 = self.cx<other.cx and [self,other] or [other,self]
		x = float(p2.cx - p1.cx)
		y = float(p2.cy - p1.cy)
		return y/x

	def similar_to(self, other):
		return (abs(self.width-other.width) < Contour.MAX_WIDTH_DIFF and
			abs(self.height-other.height) < Contour.MAX_HEIGHT_DIFF and 
			(self.avg-other.avg)/self.avg < Contour.MAX_AVG_FACTOR and
			(self.sdv-other.sdv)/self.sdv < Contour.MAX_SDV_FACTOR)
	
	def angle_to(self, other):
		a = abs(self.cx - other.cx)
		o = abs(self.cy - other.cy)
		h = math.sqrt(a*a + o*o)
		return math.asin(o/h)
				
	def potential_matches(self, contours):
		for contour in contours:
			if contour != self:
				d = self.dist_to(contour)
				if (d > self.dia*Contour.MIN_DIST_FACTOR and 
					d < self.dia*Contour.MAX_DIST_FACTOR and
					self.similar_to(contour) and
					self.angle_to(contour)<Contour.MAX_ANGLE):
					yield (contour, d)
