#!/usr/bin/env python
# -*- coding:utf-8 -*-

from . import *

class wBreak(wElement):
	"""
		Class which models a break. Commonly, a break means breakline.
	"""

	def __init__(self, breakType='page'):
		"""
			Class Constructor
		"""
		wElement.__init__(self)
		p = wParagraph(texto=None, options={})
		r = self.new_tag("w:r")
		r.append(self.new_tag("w:br", {"w:type":breakType}))
		p.add(r)
		self.bs.append(p.__bs__())
