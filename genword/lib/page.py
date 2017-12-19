#!/usr/bin/env python
# -*- coding:utf-8 -*-

from . import *

class wPage(wComponent):
	"""
		Class which models a document page
	"""

	def __init__(self):
		"""
			Class constructor.
		"""
		wComponent.__init__(self)

	def addElement(self, element):
		"""
			Add an element (wElement object) to this page

			Keyword arguments:

			element -- wElement object
		"""
		if not issubclass(element.__class__, wElement):
			raise Exception("Only 'wElement' class can be added.")
		raise Exception("Not implemented yet")