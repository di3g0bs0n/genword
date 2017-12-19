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


import random
from . import *



class wComponent(object):
	"""
		Class which models a component. Every object what can be added to a document is a component
	"""

	def __init__(self):
		"""
			Class constructor. Initializes a 'BeautifulSoup' empty object.
		"""
		self.bs = BeautifulSoup("", "lxml")

	def prettify(self):
		"""
			Returns the content of bs object (utf8 encoded)
		"""
		return self.bs.prettify("utf-8")

	def new_tag(self, tag, options={}):
		"""
			Creates a new tag

			Keyword arguments:

			tag -- Tag name
			options -- Dict with the attibutes of tag
		"""
		return self.bs.new_tag(tag, **options)

	def randomId(self, length=8):
		"""
			Returns a random Id (hex) with the length setted in the argument.

			Keyword arguments:

			length 	-- 	(Optional) Length of random string. Default 8
		"""
		return ''.join(random.choice('ABCDEF0123456789') for _ in range(length))

	def __str__(self):
		"""
			Returns the content of the bs object
		"""
		return self.prettify()

	def __unicode__(self):
		"""
			Returns the content of the bs object
		"""
		return self.prettify()

	def __bs__(self):
		"""
			Returns the bs object
		"""
		return self.bs

