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


import zipfile, tempfile, shutil, os, re, io
from bs4 import BeautifulSoup
from lib import *

class Word:

	def __init__(self):
		"""
			Class constructor. Creates a temporal directory for the document
		"""
		self.tmp = tempfile.mkdtemp()
		
	def create(self, path):
		"""
			Creates an empty document

			Keywords arguments:

			path -- Path to output document
		"""
		self.output_file = path
		filename = os.path.join(os.path.dirname(__file__), "data", "empty.dat")
		return self.load(filename)

	def load(self, path):
		"""
			Loads an existent document

			Keywords arguments:

			path -- path to document
		"""
		self.filename = path
		return self.unzip()

	def unzip(self):
		"""
			Decompress the document in a temp folder
		"""
		zip_ref = zipfile.ZipFile(self.filename, 'r')
		zip_ref.extractall(self.tmp)
		zip_ref.close()
		self.documentXml = os.path.join(self.tmp, 'word', 'document.xml')
		self.bs = BeautifulSoup(self.getDocumentContent(), "xml")
		self.documentRels = os.path.join(self.tmp, "word", "_rels", "document.xml.rels")
		f = open(self.documentRels, 'r')
		content = f.read()
		f.close()
		self.bs_rels = BeautifulSoup(content, "xml")
		target = os.path.join(self.tmp, "[Content_Types].xml")
		if os.path.isfile(target):
			self.bs_ctypes = BeautifulSoup(self.getDocumentContent(document=os.path.basename(target)), "xml")
		return self.tmp

	def zip(self, path = None):
		"""
			Join the files to a single document

			Keyword arguments:

			path -- Path to output document. If is None, then will use the path setted in "create" method
		"""
		if path is None:
			if self.output_file is not None:
				path = self.output_file
			else:
				raise Exception("No output file defined!")

		_zip = zipfile.ZipFile(path, 'w')
		for folder, subfolders, files in os.walk(self.tmp):
			for file in files:
				_zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), self.tmp), compress_type = zipfile.ZIP_DEFLATED)
 
		_zip.close()

	def getDocumentContent(self, document = None):
		"""
			Get the content of main file

			Keyword arguments

			document -- Target document. If is None, then will use the document.xml file, in other case,
						must be a file in the tmp folder created in constructor (self.tmp)
		"""
		if self.documentXml is None:
			raise Exception("Document is not unzipped")

		if document is None:
			target = self.documentXml
		else:
			target = os.path.join(self.tmp, document)

		f = io.open(target, mode="r", encoding="utf-8")
		content = f.read()
		f.close()
		return content

	def getRegexMatch(self, regex):
		"""
			Get the matchs of a document. 

			Keyword arguments:

			regex -- Regular expression to search
		"""
		content = self.getDocumentContent()
		m = re.findall(regex, content)
		return m

	def replace(self, old, new):
		"""
			Replaces a string in the main document (document.xml)

			Keyword arguments:

			old -- String to replace
			new -- New value to write
		"""
		content = self.getDocumentContent()
		new_content = content.replace(old, new)
		self.write(new_content)


	def write(self, content, file=None):
		"""
			Writes a value in the main file (document.xml)

			Keyword arguments:
			
			content -- 	Value to write in the file
			file 	--	Output file. If is None, document.xml will be used, else the relative path from self.tmp
		"""
		if file is None:
			target = self.documentXml
		else:
			target = os.path.join(self.tmp, file)

		f = io.open(target, mode="w", encoding="utf-8")
		f.write(content)
		f.close()

	def getMediaFiles(self):
		"""
			Get the filenames from "media" directory, inside document. 
		"""
		mediadir = os.path.join(self.tmp, "word", "media")
		if os.path.isdir(mediadir):
			return [f for f in os.listdir(mediadir) if os.path.isfile(os.path.join(mediadir, f))]
		return []

	def _add(self, element):
		"""
			Add an element to the document

			Keyword arguments:

			element -- wElement object
		"""
		if not issubclass(element.__class__, wElement):
			raise Exception("Only wElement can be added")
		try:	
			body = self.bs.findAll("w:body")[0]
		except IndexError:
			raise Exception("document.xml malformed")

		secPr = body.findAll("w:sectPr")[-1]
		if issubclass(secPr.__class__, Tag):
			secPr.insert_before(element.__bs__())
		else:
			body.append(element.__bs__())

	def add(self, element):
		"""
			Add an element to the document

			Keyword arguments:

			element -- wElement object
		"""
		
		if issubclass(element.__class__, wImage):
			self.addImage(element)
			
		else:
			self._add(element)

	def addImage(self, image):
		"""
			Add an image to the document

			Keyword arguments

			image -- [String | wImage] If is String, then a wImage object will be instanced
		"""
		if type(image) == type(str()):
			image = wImage(image)
		elif not issubclass(image.__class__, wImage):
			raise Exception("Only wImage can be added")

		self._add(image)

		# Build Relationships
		
		files = self.getMediaFiles()
		numbers = [0]
		for f in files:
			rse = re.search("image(\d)\..*", f)
			if rse:
				numbers.append(int(rse.group(1)))

		nextName = "image%d.%s" % (max(numbers) + 1, image.ext)
		image.setBasename(nextName)
		relationships = self.bs_rels.findAll("Relationship")
		nextId = "rId%s" % (max(map(lambda x: int(x['Id'].replace('rId','')), relationships)) + 1)
		image.setId(nextId)
		image.setup(self.tmp)
		self.bs_rels.findAll('Relationships')[0].append(image.getRelationship())
		self.write(unicode(self.bs_rels.prettify("utf-8")), 'word/_rels/document.xml.rels')

	def dump(self):
		"""
			Write the 'bs' content in the document.xml file
		"""
		self.write(unicode(self))

	def addContentType(self, ext, ctype):
		"""
			Add a Content Type to file [Content_Types.xml]

			Keyword arguments:

			ext 	--	File extension
			ctype 	--	Content Type
		"""
		self.bs_ctypes.find("Types").append(self.bs_ctypes.new_tag("Default", **{"Extension":ext, "ContentType":ctype}))
		self.write(unicode(self.bs_ctypes.prettify("utf-8")), '[Content_Types].xml')

	def clean(self):
		"""
			Clean up
		"""
		try:
			import shutil
		except:
			pass
		shutil.rmtree(self.tmp)

	def __del__(self):
		"""
			Clean up
		"""
		self.clean()

	def __str__(self):
		"""
			Returns the content of document.xml
		"""
		return self.bs.prettify("utf-8")

	def __unicode__(self):
		"""
			Returns the content of document.xml
		"""
		return self.bs.prettify("utf-8")

	def __bs__(self):
		"""
			Returns a BS Object with the content of document.xml
		"""
		if self.bs is None:
			raise Excpetion("Document not unzipped")
		return self.bs


if __name__ == "__main__":

	print "*** TESTING ***"

	w = Word()
	w.create('/tmp/example.docx')
	w.addContentType(ext="png", ctype="image/png")
	w.addContentType(ext="jpg", ctype="image/jpeg")
	ph = wParagraph("Hola mundo")
	ph2 = wParagraph("Hola mundo2")
	w.add(ph)
	w.add(ph2)
	br = wBreak()
	w.add(br)
	ph = wParagraph("Hola mundfsddo")
	ph2 = wParagraph("Hola mundsdfsdo2")
	w.add(ph2)
	w.add(ph)
	br = wBreak()
	w.add(br)
	
	


	t = wTable()
	t.setBorders()

	r = wTableRow(columns=2)
	r.setAlign("center")

	hoptions = {"size":"28", "sizeCs": "21", "color": "00C6DA", "align":"center", "smallCaps": True, "bold": True}
	width = 15000 / 4
	texto1 = wParagraph(u"URLs", hoptions)
	texto2 = wParagraph(u"Params", hoptions)
	c1 = wTableCell({"bgcolor":"2C6584", "width":width*3});c1.setText(texto1)
	c2 = wTableCell({"bgcolor":"2C6584", "width":width});c2.setText(texto2)
	r.addCells([c1, c2])
	t.addRow(r)

	
	i = wImage('/tmp/logo.png')
	br = wBreak()

	w.add(i)
	w.add(br)
	w.addImage("/tmp/img_profile.jpg")

	w.dump()
	w.zip()

	print str(w)