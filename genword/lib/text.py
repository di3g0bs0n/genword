#!/usr/bin/env python
# -*- coding:utf-8 -*-

from . import *

class wText(wComponent):

	def __init__(self, texto, options = {}):
		wComponent.__init__(self)
		self.element = self.new_tag("w:r", {"w:rsidRPr": "00F86726"})
		self.bs.append(self.element)
		self.properties = self.new_tag("w:rPr")
		self.element.append(self.properties)

		self.setProperties(options)
		self.textElement = self.new_tag("w:t")
		self.textElement.string = texto
		self.element.append(self.textElement)


	def _addProperty(self, element, attr = {}):
		self.properties.append(self.new_tag(element, attr))


	def setProperties(self, options = {}):
		if "bold" in options.keys():
			self._addProperty("w:b")
		if "smallCaps" in options.keys():
			self._addProperty("w:smallCaps")
		if "color" in options.keys():
			self._addProperty("w:color", {"w:val": options['color']})
		if "size" in options.keys():
			self._addProperty("w:sz", {"w:val": options['size']})
		if "sizeCs" in options.keys():
			self._addProperty("w:szCs", {"w:val": options['sizeCs']})
		if "lang" in options.keys():
			self.__addProperty("w:lang", {"w:val": options['lang']})


