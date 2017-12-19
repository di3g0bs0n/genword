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
import math


class wTable(wElement):

	def __init__(self, options={"columns": 4}):
		"""
			Class contructor. Build the table. 

			Keyword arguments:

			options 	-- (Optional) Dict with table properties (See "setProperties" doc)

		"""
		wElement.__init__(self)
		self.element = self.new_tag("w:tbl")
		self.bs.append(self.element)
		self.properties = self.new_tag("w:tblPr")
		self.element.append(self.properties)

		self.setProperties(options)
		self._tblLook()
		try:
			self._tblGrid(options['columns'])
			self.columns = options['columns']
		except KeyError:
			self._tblGrid()

	def _tblLook(self):
		"""
			Set the table look
		"""
		attr = {
			"w:val": "04A0",
			"w:firstRow": "1",
			"w:lastRow": "0",
			"w:lastColumn": "0",
			"w:noHBand": "0",
			"w:noVBand": "1"
		}
		item = self.new_tag("w:tblLook", attr)
		self.properties.append(item)

	def _tblGrid(self, columns = 4):
		"""
			Set the table grid. Defines the columns width

			Keyword arguments:

			columns 	--	(Optional) Number of columns. Default = 4
		"""
		w_total = 12000
		col_w = int(math.ceil(w_total / columns))
		grid = self.new_tag("w:tblGrid")
		for i in range(0,columns):
			col = self.new_tag("w:gridCol", {"w:w": col_w})
			grid.append(col)
		self.element.append(grid)

	def _addProperty(self, element, attr = {}):
		"""
			Add an element into properties tag

			Keyword arguments:

			element 	-- 	Tag name
			attr 		--	(Optional) Dict with tag attributes
		"""
		self.properties.append(self.new_tag(element, attr))

	def setProperties(self, options = {}):
		"""
			Set the table properties.

			Keyword arguments:

			options 	--	(Optional) Dict with properties and values.

			Available Options:
				* align
				* border
		"""
		if "align" in options.keys():
			self._addProperty("w:jc", {"w:val": options['align']})
		if "border" in options.keys():
			self.setBorders(options['border'])

	def setBorders(self, color = "D9D9D9"):
		"""
			Set the table borders.

			Keyword arguments:

			color 	--	(Optional) Borders color
		"""
		self.borders = self.new_tag("w:tblBorders")
		attrs = {
			"w:val": "single",
			"w:sz": "12",
			"w:space": "0",
			"w:color": color,

		}
		self.borders.append(self.new_tag("w:top", attrs))
		self.borders.append(self.new_tag("w:left", attrs))
		self.borders.append(self.new_tag("w:bottom", attrs))
		self.borders.append(self.new_tag("w:right", attrs))
		self.borders.append(self.new_tag("w:insideH", attrs))
		self.borders.append(self.new_tag("w:insideV", attrs))

		self.properties.append(self.borders)

	def addRow(self, row):
		"""
			Add a row to the table.

			row 	--	wTableRow object
		"""
		if not issubclass(row.__class__, wTableRow):
			raise Exception("Only wTableRow can be added")
		self.element.append(row.__bs__())


		
