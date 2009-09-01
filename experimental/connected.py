#!/usr/bin/env python
# encoding: utf-8
"""
connected.py

A pure python connected components algorithm.

Created by Oliver Smith on 2009-08-31.
Copyright (c) 2009 Oliver Smith. All rights reserved.
"""

import cv

class DisjointSetTree(object):
	"""A disjoint set tree data structure.
	
	See http://en.wikipedia.org/wiki/Disjoint-set_data_structure
	
	"""
	
	def __init__(self):
		"""ctor."""
		self.parent = self
		self.rank = 0
		self.value = 0
	
	def union(self, other):
		"""Union with another tree."""
		s_root = self.find()
		o_root = other.find()
		if s_root.rank > o_root.rank:
			o_root.parent = s_root
		elif o_root.rank > s_root.rank:
			s_root.parent = o_root
		elif o_root != s_root:
			o_root.parent = s_root
			s_root.rank += 1
	
	def find(self):
		"""Find the root of the tree."""
		if self.parent == self:
			return self
		else:
			self.parent = self.parent.find()
			return self.parent


def connected(image):
	"""Get connected components of an image.
	
	Returns a coloured image.
	"""
	# check the depth and number of channels is correct
	if image.depth != 8 or image.nChannels != 1:
		# todo: raise an exception
		return None
	# first scan - label all the components
	intermediate = []
	prev_row = None
	for y in range(image.height):
		row = []
		for x in range(image.width):
			if int(image[y,x]) > 0:
				value = DisjointSetTree()
				neighbours = []
				if y > 0:
					top = prev_row[x]
					if top != None:
						neighbours += [top]
				if x > 0:
					left = row[-1]
					if left != None:
						neighbours += [left]
				for neighbour in neighbours:
					value.union(neighbour)
				row += [value]
			else:
				row += [None]
		intermediate += [row]
		prev_row = row
	# second scan - number all the distinct components
	counter = 0
	for row in intermediate:
		for value in row:
			if value is not None and value.parent == value:
				counter += 1
				value.value = counter
	# third scan - create a coloured image
	output = cv.CreateImage((image.width,image.height), cv.IPL_DEPTH_8U, 1)
	y = 0
	for row in intermediate:
		x = 0
		for value in row:
			if value is None:
				output[y,x] = 0
			else:
				output[y,x] = value.find().value % 256
			x += 1
		y += 1
	# done!
	return output


