#!/usr/bin/env python3
'''
	Copyright (C) 2023 Minho Jo <whitestone8214@gmail.com>

	Permission is hereby granted, free of charge, to any person obtaining a copy
	of this software and associated documentation files (the "Software"), to deal
	in the Software without restriction, including without limitation the rights
	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
	copies of the Software, and to permit persons to whom the Software is
	furnished to do so, subject to the following conditions:
	
	The above copyright notice and this permission notice shall be included in all
	copies or substantial portions of the Software.
	
	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
	SOFTWARE.
'''


# External module(s)
import pyglet

# Builtin module(s)
import sys, os, datetime


class M2Label(pyglet.text.DocumentLabel):
	def __init__(self):
		from pyglet.text.formats import html
		
		# (document, x, y, width, height, anchor_x, anchor_y, multiline, dpi, batch, group)
		# See more at "class DocumentLabel"
		self._text = ""
		self._location = None
		self._decoder = html.HTMLDecoder()
		super(M2Label, self).__init__(self._decoder.decode("", self._location), 0, 0, 1, 1, "left", "top", True, None, None, None)
		
	def decode(self):
		self.document = self._decoder.decode(self._text, self._location)
		return self
		
	def x(self, value):
		self._x = value
		return self
		
	def y(self, value):
		self._y = value
		return self
		
	def widthBox(self, value):
		self._width = value
		return self
		
	def heightBox(self, value):
		self._height = value
		return self
		
	def alignX(self, value):
		self.set_style("align", value)
		self._anchor_x = value
		return self
		
	def alignY(self, value):
		self.set_style("valign", value)
		self._anchor_y = value
		return self
		
	def multiline(self, value):
		self._multiline = value
		return self
		
	def text(self, value):
		self._text = value
		return self
