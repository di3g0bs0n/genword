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

class wParagraph(wElement):

	def __init__(self, texto = None, options = {"font": "Calibri", "size": "12", "align":"left"}):
		"""
			Class constructor. Build the paragraph.

			Keyword options:

			texto 	-- 	(Optional) Text to write into paragraph. Default None
			options --	(Optional) Dict with paragraph properties (See "setProperties" doc). Default {"font": "Calibri", "size": "12", "align":"left"}
		"""
		wElement.__init__(self)
		r1 = self.randomId(8)
		attr = {
			"w14:paraId": self.randomId(8),
			"w14:textId": self.randomId(8),
			"w:rsidR": r1,
			"w:rsidRPr": r1,
			"w:rsidRDefault": r1,
			"w:rsidP": self.randomId(8)
		}
		self.element = self.new_tag("w:p", attr)
		self.bs.append(self.element)
		self.properties = self.new_tag("w:pPr")
		self.element.append(self.properties)
		self.rproperties = self.new_tag("w:rPr")
		self.properties.append(self.rproperties)

		self.setProperties(options)
		if texto is not None:
			t = wText(texto, options)
			self.element.append(t.__bs__())

	def add(self, component):
		"""
			Add a component into the paragraph

			component 	-- wComponent Object
		"""
		if not issubclass(component.__class__, wComponent):
			if not issubclass(component.__class__, Tag):
				raise Exception("Only wComponent or bs4.element.Tag can be added to wParagraph")
			else:
				self.element.append(component)
		else:
			self.element.append(component.__bs__())

	def _addProperty(self, element, attr = {}):
		"""
			Add a new tag in the pPr tag

			element 	-- 	Tag name
			attr		--	(Optional) Dict with tag attributes
		"""
		self.properties.append(self.new_tag(element, attr))

	def _addRProperty(self, element, attr = {}):
		"""
			Add a new tag in the rPr tag

			element 	-- 	Tag name
			attr		--	(Optional) Dict with tag attributes
		"""
		self.rproperties.append(self.new_tag(element, attr))

	def setProperties(self, options = {}):
		"""
			Set the Paragraph properties

			Keyword arguments:

			options 	-- (Optional) Dict with options. Default {}

			Available Options:

				* align
				* bold
				* smallCaps
				* color
				* size
				* sizeCs
				* lang
				* font
		"""
		if "align" in options.keys():
			self._addProperty("w:jc", {"w:val": options['align']})
		if "bold" in options.keys():
			self._addRProperty("w:b")
		if "smallCaps" in options.keys():
			self._addRProperty("w:smallCaps")
		if "color" in options.keys():
			self._addRProperty("w:color", {"w:val": options['color']})
		if "size" in options.keys():
			self._addRProperty("w:sz", {"w:val": options['size']})
		if "sizeCs" in options.keys():
			self._addRProperty("w:szCs", {"w:val": options['sizeCs']})
		if "lang" in options.keys():
			self.__addRProperty("w:lang", {"w:val": options['lang']})
		if "font" in options.keys():
			self._addRProperty("w:rFonts", {"w:ascii": options['font'], "w:hAnsi": options['font']})

