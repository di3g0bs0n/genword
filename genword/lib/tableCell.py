#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author: Diego Fernández <di3g0bs0n@gmail.com>

# MIT License
# Copyright (c) 2017 di3g0bs0n

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from . import * 

class wTableCell(wComponent):

	def __init__(self, options={"width": 2000, "bgcolor": "FFFFFF"}):
		"""
			Class constructor. Build de Cell.

			Keyword arguments:

			options 	--	(Optional) Dict with Cell properties

			Available properties:
				* bgcolor = FFFFFF
				* width = 2000
		"""
		wComponent.__init__(self)

		try:
			width = options['width']
		except KeyError:
			width = 2000
		try:
			bgcolor = options['bgcolor']
		except KeyError:
			bgcolor = "FFFFFF"


		self.element = self.new_tag("w:tc")
		self.bs.append(self.element)

		self.properties = self.new_tag("w:tcPr")
		self.addProperty("w:tcW", {"w:type":"dxa", "w:w": width})
		self.addProperty("w:shd", {"w:val":"clear", "w:color": "auto", "w:fill":bgcolor})
		self.addProperty("w:vAlign", {"w:val":"center"})

		self.element.append(self.properties)

	def addProperty(self, element, attr={}):
		"""
			Add a new tag in the properties tag

			Keyword arguments:

			element 	-- 	Tag name
			attr 		-- 	(Optional) Dict with tag attributes
		"""
		self.properties.append(self.new_tag(element, attr))

	def setText(self, textElement):
		"""
			Set the cell text. Actually, add a wParagraph object inside the cell.

			Keyword arguments:

			textElement 	--	wParagraph object.
		"""
		if not issubclass(textElement.__class__, wParagraph):
			raise Exception("Only wParagraph can be added to a wTableCell")

		self.element.append(textElement.__bs__())

	def setVMerge(self, restart=False):
		"""
			Merge the Cell vertically. For the cells in the same column, the first cell must have restart=True. 
			The following cells with VMerge, but restart=False, will be merged.

			Keyword arguments:

			restart 	-- (Optional) Indicates the start of a new combined cell
		"""
		if restart:
			self.properties.append(self.new_tag("w:vMerge", {"w:val":"restart"}))
		else:
			self.properties.append(self.new_tag("w:vMerge"))
