#!/usr/bin/env python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from . import *

class wElement(wComponent):
	"""
		Class which models an element. Every object what can be added to a page, is an element.
	"""

	def __init__(self):
		wComponent.__init__(self)

	