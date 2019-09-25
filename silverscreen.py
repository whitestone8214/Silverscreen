#!/usr/bin/env python3
'''
	Copyright (C) 2018-2019 Minho Jo <whitestone8214@gmail.com>
	
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.
	
	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.
	
	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


# External module(s)
from pyglet import pyglet
from pyjson5 import json5

# Builtin module(s)
import sys, os, datetime


# In-here routine(s)
def load_sheet(path):
	print('LOAD ' + path)
	_file = open(path, 'r')
	_sheet = json5.load(_file)
	_file.close()
	return _sheet


_path = sys.argv[1] # Path to file to load
_sheet = load_sheet(_path) # Sheet generated from file
_here = -1 # Page number current we are in

_screenMain = pyglet.canvas.get_display().get_default_screen()
_span1 = (_screenMain.width < _screenMain.height) and (_screenMain.width / 20) or (_screenMain.height / 20)
_span2 = (_span1 / 4) * 3
_windowMain = pyglet.window.Window()
pyglet.gl.glClearColor(1, 1, 1, 1)
_windowMain.toShow = None
_windowMain.redraw = False

# Main window
_windowMain.standard = 0
_windowMain.inputStacked = ''
_windowMain.nEscPressed = 0
_dictPages = None

# Load session
if 'standard' in _sheet: _windowMain.standard = _sheet['standard']
if 'pages' not in _sheet: raise Exception('No pages to show')
_dictPages = _sheet['pages']
print(str(len(_dictPages)) + ' page(s)')


# Non-trigger functions
def textboxV1(_width, _height, _x, _y, text, colorText, alignmentX, alignmentY):
	_textbox = pyglet.text.HTMLLabel(
		text,
		width = _width, height = _height,
		x = _x, y = _windowMain.height - _y,
		anchor_x = alignmentX, anchor_y = alignmentY,
		multiline = True
	)
	_textbox.set_style('font_name', 'Source Han Sans KR')
	#_textbox.set_style('font_size', sizeDefault)
	return _textbox
def textboxV2(_width, _height, _x, _y, text, colorText, alignmentX, alignmentY):
	_textbox = pyglet.text.HTMLLabel(
		text,
		width = _width, height = _height,
		x = _x, y = _windowMain.height - _y,
		anchor_x = alignmentX, anchor_y = alignmentY,
		multiline = True
	)
	_textbox.set_style('font_name', 'Source Han Sans KR')
	#_textbox.set_style('font_size', sizeDefault)
	return _textbox
def picture(address, width, height):
	_path = address
	if os.name == 'nt': _path = _path.replace('/', '\\')
	_picture = pyglet.image.load(_path)
	#if width >= 1 and height >= 1: _picture = _picture.get_region(0, _picture.height - 1 - int(height), int(width), int(height))
	return _picture
def show_page(_type, background, title, body):
	_type0 = str(_type); _title = str(title); _body = str(body)
	
	# Background
	try:
		_picture = pyglet.image.load(os.getcwd() + (os.name == 'nt' and '\\' or '/') + background)
		if _type0 != 'lyrics':
			_picture = _picture.get_region(0, _windowMain.height - int(_span1 * 2), _picture.width, int(_span1 * 2))
			_picture.blit(0, _windowMain.height - int(_span1 * 2), 0, _windowMain.width, _span1 * 2)
		else: _picture.blit(0, 0, 0, _windowMain.width, _windowMain.height)
	except: print('BACKGROUND FAILED')
	
	# Title
	try: textboxV2(_windowMain.width, _span1, _span1 / 4, _span1 / 2, '<font size="' + str(_span1) + '" color="#ffffff">' + _title + '</font>', (255, 255, 255, 255), 'left', 'center').draw()
	except: print('TITLE FAILED')
	
	# Body
	try:
		if _type0 == 'cover':
			textboxV2(
				#_windowMain.width, _windowMain.height - (_span1 * 2),
				_windowMain.width, 1,
				0, (_windowMain.height / 2) + _span1,
				'<p align="center"><font size="' + str(_span1) + '">' + _body + '</font></p>', (255, 255, 255, 255),
				'left', 'center2'
			).draw()
		else:
			textboxV2(
				_windowMain.width, _span1,
				_span1 / 4, _span1 * 2,
				'<font size="' + str(_span1) + '">' + _body + '</font>', (255, 255, 255, 255),
				'left', 'top'
			).draw()
	#except: print('BODY FAILED')
	except: raise Exception
			

# Triggers
@_windowMain.event
def on_draw():
	if _windowMain.redraw != True:
		_windowMain.redraw = False
		return pyglet.event.EVENT_HANDLED
	
	_valueType = None
	try: _valueType = _windowMain.toShow['type']
	except: None
	_valueBackground = None
	try: _valueBackground = _windowMain.toShow['background']
	except: None
	_valueTitle = None
	try: _valueTitle = _windowMain.toShow['title']
	except: None
	_valueBody = None
	try: _valueBody = _windowMain.toShow['body']
	except: None
	
	_windowMain.clear()
	show_page(_valueType, _valueBackground, _valueTitle, _valueBody)
	
	_windowMain.redraw = False
	
	'''
	pyglet.text.Label(
		str(_valueTitle),
		font_name = 'Source Han Sans KR', font_size = 36,
		x = _windowMain.width // 2, y = _windowMain.height // 2,
		anchor_x = 'center', anchor_y = 'center',
	).draw()
	'''
@_windowMain.event
def on_key_press(value, modifiers):
	# Force use global ones about these
	global _path
	global _sheet
	global _here
	global _dictPages
	
	# Just for debugging
	#print('KEY ' + str(value) + ' (' + chr(value) + ')')
	#print('MOD ' + str(modifiers))
	
	if modifiers == 2 and value == 114: # Ctrl + R: Reload the file
		_windowMain.nEscPressed = 0
		_hereRemember = _here
		_sheet = load_sheet(_path)
		if 'standard' in _sheet: _windowMain.standard = _sheet['standard']
		if 'pages' not in _sheet: raise Exception('No pages to show')
		_dictPages = _sheet['pages']
		_here = _hereRemember
		_windowMain.redraw = True
	elif value >= 48 and value <= 57: # Number
		_windowMain.nEscPressed = 0
		if value != None: _windowMain.inputStacked += chr(value)
		return pyglet.event.EVENT_HANDLED
	elif value >= 97 and value <= 122: # Alphabet
		_windowMain.nEscPressed = 0
		if value != None: _windowMain.inputStacked += chr(value)
		return pyglet.event.EVENT_HANDLED
	elif value == 65293: # Enter: Send the order
		_windowMain.nEscPressed = 0
		_order = _windowMain.inputStacked
		#if _windowMain.inputStacked != None: print('ORDER ' +  _windowMain.inputStacked)
		if _order in _dictPages: _here = list(_dictPages.keys()).index(_order)
		else:
			_here1 = -1
			try: _here1 = int(_order) - 1
			except: _here1 = -1
			
			if _here1 >= 0 and _here1 < len(_dictPages): _here = _here1
			else: print('ERROR NO_SUCH_ORDER')
			
		if _here != -1:
			#print('PAGE ' + str(_here))
			_windowMain.toShow = list(_dictPages.values())[_here]
			_windowMain.redraw = True
		_windowMain.inputStacked = ''
	elif value == 65307: # Escape: Cancel the order
		_windowMain.inputStacked = ''
		if _windowMain.nEscPressed >= 2: None
		else:
			_windowMain.nEscPressed += 1
			print('SAY ESC pressed ' + str(_windowMain.nEscPressed) + ' time(s)')
			return pyglet.event.EVENT_HANDLED
	elif value == 65361: # Left arrow: Previous page
		_windowMain.nEscPressed = 0
		_here -= 1
		if _here < 0: _here = 0
		_windowMain.toShow = list(_dictPages.values())[_here]
		_windowMain.redraw = True
	elif value == 65363: # Right arrow: Next page
		_windowMain.nEscPressed = 0
		_here += 1
		if _here >= len(_dictPages): _here = len(_dictPage) - 1
		_windowMain.toShow = list(_dictPages.values())[_here]
		_windowMain.redraw = True
	elif value == 65360: # Home: First page
		_windowMain.nEscPressed = 0
		_here = 0
		_windowMain.toShow = list(_dictPages.values())[_here]
		_windowMain.redraw = True
	elif value == 65367: # End: Last page
		_windowMain.nEscPressed = 0
		_here = len(_dictPages) - 1
		_windowMain.toShow = list(_dictPages.values())[_here]
		_windowMain.redraw = True
	elif value == 65474: # F5: Fullscreen ON/OFF
		_windowMain.nEscPressed = 0
		_windowMain.set_fullscreen(_windowMain.fullscreen == False)
		_windowMain.redraw = True
	else:
		_windowMain.nEscPressed = 0
		print('KEY ' + str(value) + ' (' + chr(value) + ')')
		#return pyglet.event.EVENT_HANDLED
		
	# It seems on_draw would be triggered automatically after this


# Go!
pyglet.app.run()
