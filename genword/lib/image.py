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


import string, shutil, random, os
from PIL import Image  

from . import *

class wImage(wElement):

	def __init__(self, image_path):
		"""
			Class contstructos. Creates image object.

			Keyword arguments:

			image_path 	--	Path to image
		"""
		wElement.__init__(self)
		self.path = image_path
		self.randomId = self.randomId(8)
		
		try:
			self.ext = image_path.split(".")[-1].lower()
		except:
			self.ext = "jpg"

		cx, cy = Image.open(self.path).size
		self.cx = cx * 10000
		self.cy = cy * 10000
		print self.cx
		print self.cy

		self.basename = "%s.%s" % (''.join(random.choice(string.ascii_lowercase) for _ in range(6)), self.ext)
		self.id = "rId" + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
		self.relType = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"
		self.buildRelationship()
		self.build()

	def buildRelationship(self):
		"""
			Build the relationship object
		"""
		attr = {"Type": self.relType, "Target": os.path.join("media", self.basename), "Id": self.id}
		self.rel = self.new_tag("Relationship", attr)

	def getRelationship(self):
		"""
			Returns the relationship object
		"""
		return self.rel

	def setup(self, directory):
		"""
			Copy the image to the media directory, inside the document.
			The image will be copied into "word/media", inside the directory setted.

			Keyword arguments:

			directory 	--	Full path to tmp directory for the document.
			
		"""
		working_dir = os.path.join(directory, "word")
		media_dir = os.path.join(working_dir, "media")
		target_path = os.path.join(media_dir, self.basename)

		if os.path.isdir(working_dir):
			if not os.path.exists(media_dir):
				os.makedirs(media_dir)
			
			shutil.copyfile(self.path, target_path)
		else:
			raise Exception("Document not unzipped")

	def setId(self, id):
		"""
			Set the id. This is will be user in order to create relationships

			id 	-- Relationship id
		"""
		blip = self.bs.find('a:blip')
		blip["r:embed"] = id
		self.rel['Id'] = id

	def setBasename(self, basename):
		"""
			Set the image basename

			basename 	-- Image basename
		"""
		self.rel['Target'] = os.path.join("media", basename)
		pic = self.bs.find("pic:cNvPr")
		pic["name"] = basename
		self.basename = basename

	def build(self):
		"""
			Build the Image Tag.
		"""
		self.element = self.new_tag("w:drawing")
		inline = self.new_tag("wp:inline", {"distT":"0", "distB":"0", "distL":"0", "distR":"0","wp14:anchorId": self.randomId, "wp14:editId": self.randomId
			})
		inline.append(self.new_tag("wp:extent", {"cx": self.cx,"cy":self.cy}))
		inline.append(self.new_tag("wp:effectExent", {"l":"0", "t":"0", "r":"0", "b":"0"}))
		a = self.new_tag("wp:docPr", {"id":"1"})
		a["name"] = "Imagen 1"
		inline.append(a)
		item = self.new_tag("wp:cNvGraphicFramePr")
		item.append(self.new_tag("a:graphicFrameLocks", {"xmlns:a":"http://schemas.openxmlformats.org/drawingml/2006/main", "noChangeAspect":"1"}))
		inline.append(item)
		
		graphic = self.new_tag("a:graphic", {"xmlns:a":"http://schemas.openxmlformats.org/drawingml/2006/main"})
		graphicData = self.new_tag("a:graphicData", {"uri":"http://schemas.openxmlformats.org/drawingml/2006/picture"})
		graphic.append(graphicData)
		inline.append(graphic)


		pic = self.new_tag("pic:pic", {"xmlns:pic":"http://schemas.openxmlformats.org/drawingml/2006/picture"})
		graphicData.append(pic)

		picPr = self.new_tag("pic:nvPicPr")
		a = self.new_tag("pic:cNvPr", {"id":"1"})
		a["name"] = self.basename
		picPr.append(a)
		picPr.append(self.new_tag("pic:cNvPicPr"))
		pic.append(picPr)

		blip = self.new_tag("pic:blipFill")
		a_blip = self.new_tag("a:blip", {"r:embed":self.id})
		blip.append(a_blip)
		stretch = self.new_tag("a:stretch")
		stretch.append(self.new_tag("a:fillRect"))
		blip.append(stretch)
		pic.append(blip)

		spPr = self.new_tag("pic:spPr")
		xfrm = self.new_tag("a:xfrm")
		xfrm.append(self.new_tag("a:off",{"x":"0","y":"0"}))
		xfrm.append(self.new_tag("a:ext",{"cx": self.cx,"cy":self.cy}))
		prstGeom = self.new_tag("a:prstGeom", {"prst":"rect"})
		prstGeom.append(self.new_tag("a:avLst"))
		spPr.append(xfrm)
		spPr.append(prstGeom)
		pic.append(spPr)

		self.element.append(inline)
		self.bs.append(self.element)







