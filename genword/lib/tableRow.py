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

class wTableRow(wComponent):

	def __init__(self, align="center", columns=4):
		"""
			Class constructor. Build the row.

			Keyword arguments:

			align 	-- (Optional) Text alignment. Default "center"
			columns -- (Optional) Numbers of columns. Default 4
		"""
		wComponent.__init__(self)
		attr = {
			"w:rsidR": self.randomId(8),
			"w:rsidRPr": self.randomId(8),
			"w14:paraId": self.randomId(8),
			"w14:textId": self.randomId(8),
			"w:rsidTr": self.randomId(8)
		}
		self.element = self.new_tag("w:tr", attr)
		self.bs.append(self.element)
		self.properties = self.new_tag("w:trPr")
		self.addProperty("w:jc", {"w:val": align})

	def addProperty(self, element, attr={}):
		"""
			Add a new tag into properties tag

			Keyword arguments:

			element 	-- Tag name
			attr 		-- (Optional) Dict with tag attributes
		"""
		self.properties.append(self.new_tag(element, attr))

	def addCell(self, cell):
		"""
			Add a cell to this row

			Keyword arguments:

			cell 	-- wTableCell object
		"""
		if not issubclass(cell.__class__, wTableCell):
			raise Exception("Only wTableCell can be added to a wTableRow")
		self.element.append(cell.__bs__())

	def addCells(self, cells = []):
		"""
			Add cells into this row

			Keyword arguments:

			cells 	-- (Optional) List of wTableCell objects
		"""
		for cell in cells:
			if not issubclass(cell.__class__, wTableCell):
				raise Exception("Only wTableCell can be added to a wTableRow")
			self.addCell(cell)

	def setAlign(self, value="left"):
		"""
			Set the text elign for this Row

			value 	-- 	(Optional) Value of alignment. Default "left"
		"""
		attr = {
			"w:val": value
		}
		pr = self.new_tag("w:trPr")
		pr.append(self.new_tag("w:jc", attr))
		self.element.append(pr)
