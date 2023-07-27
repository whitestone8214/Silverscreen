#!/usr/bin/env python3
'''
	Copyright (C) 2018-2023 Minho Jo <whitestone8214@gmail.com>
	
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


# Inhouse module(s)
from side import M2Label

# External module(s)
import pyglet, json5

# Builtin module(s)
import sys, os, datetime


# In-here routine(s)
def load_sheet(path):
	_file = open(path, 'r')
	_sheet = json5.load(_file)
	_file.close()
	return _sheet


# Sheet
_path = sys.argv[len(sys.argv) - 1] # Path to file to load
_sheet = load_sheet(_path) # Sheet generated from file
_here = -1 # Page number current we are in

# Screen and window
_listScreens = pyglet.canvas.get_display().get_screens()
_screen = _listScreens[0] # Display to use as basis
_widthWindow = (_screen.width / 4) * 3
_heightWindow = (_screen.height / 4) * 3
_xWindow = _screen.width / 8
_yWindow = _screen.height / 8
_modeFrameless = False
_span1 = (_screen.width < _screen.height) and (_screen.width / 16) or (_screen.height / 16)
_span2 = (_span1 / 4) * 3
_fontDefault = "Noto Sans CJK KR"

# Apply the commandline option(s), if any
for _nthOption in range(0, len(sys.argv) - 1):
	_option = sys.argv[_nthOption]
	if _option.startswith("-screen="):
		_nthScreen = 0
		try:
			_nthScreen = int(_option[8:])
		except:
			print("[Silverscreen] ERROR: Non-valid number value given with -screen=; Will use screen #0")
			continue
		if _nthScreen == -1:
			_screen = _listScreens[len(_listScreens) - 1]
		elif _nthScreen >= len(_listScreens):
			print("[Silverscreen] ERROR: You ordered screen #" + str(_nthScreen) + ", but this system has " + str(len(_listScreens)) + " screen(s); Will use screen #0")
			continue
		_screen = _listScreens[_nthScreen]
	elif _option.startswith("-width="):
		_widthWindowNew = _widthWindow
		try:
			_widthWindowNew = int(_option[7:])
		except:
			print("[Silverscreen] ERROR: Non-valid number value given with -width=; Will use 3/4 of screen width")
			continue
		if _widthWindowNew == -1:
			_widthWindowNew = _screen.width
		elif _widthWindowNew < 1:
			print("[Silverscreen] ERROR: Window width must be 1px or more; Will use 3/4 of screen width")
			continue
		_widthWindow = _widthWindowNew
	elif _option.startswith("-height="):
		_heightWindowNew = _heightWindow
		try:
			_heightWindowNew = int(_option[8:])
		except:
			print("[Silverscreen] ERROR: Non-valid number value given with -height=; Will use 3/4 of screen height")
			continue
		if _heightWindowNew == -1:
			_heightWindowNew = _screen.height
		elif _heightWindowNew < 1:
			print("[Silverscreen] ERROR: Window height must be 1px or more; Will use 3/4 of screen height")
			continue
		_heightWindow = _heightWindowNew
	elif _option.startswith("-x="):
		_xWindowNew = _xWindow
		try:
			_xWindowNew = int(_option[3:])
		except:
			print("[Silverscreen] ERROR: Non-valid number value given with -x=; Will use 1/8 of screen width")
			continue
		_xWindow = _xWindowNew
	elif _option.startswith("-y="):
		_yWindowNew = _yWindow
		try:
			_yWindowNew = int(_option[3:])
		except:
			print("[Silverscreen] ERROR: Non-valid number value given with -y=; Will use 1/8 of screen height")
			continue
		_yWindow = _yWindowNew
	elif _option == "-frameless":
		_modeFrameless = True

# Main window
_windowMain = pyglet.window.Window(
	width = int(_widthWindow),
	height = int(_heightWindow),
	caption = "Silverscreen: " + os.path.basename(_path),
	style = _modeFrameless is True and pyglet.window.BaseWindow.WINDOW_STYLE_BORDERLESS or None
)
_windowMain.set_location(int(_xWindow), int(_yWindow))
pyglet.gl.glClearColor(1, 1, 1, 1)
_windowMain.toShow = None
_windowMain.redraw = False
_windowMain.standard = 0
_windowMain.inputStacked = ''
_windowMain.nEscPressed = 0
_windowMain.listPages = None
_windowMain.listKeyPages = [None, None, None, None, None, None, None, None, None, None]

# Load session
if 'standard' in _sheet: _windowMain.standard = _sheet['standard']
if 'pages' not in _sheet: raise Exception('No pages to show')
_windowMain.listPages = _sheet['pages']

# Find and register key page(s)
for _x in _windowMain.listPages:
	_page = _windowMain.listPages[_x]
	if "key" in _page:
		_value = int(_page['key'])
		if _value >= 0 and _value <= 9:
			print("SAY key_found " + _page['key'])
			_windowMain.listKeyPages[_value] = _x

#print(str(len(_windowMain.listPages)) + ' page(s)')


# Non-trigger functions
def picture(address, width, height):
	_path = address
	if os.name == 'nt': _path = _path.replace('/', '\\')
	_picture = pyglet.image.load(_path)
	#if width >= 1 and height >= 1: _picture = _picture.get_region(0, _picture.height - 1 - int(height), int(width), int(height))
	return _picture
def show_page(_type, background, title, body):
	_type0 = str(_type)
	if (_type0 == "p2"):
		if _windowMain.inputStacked == '':
			try: print("[Silverscreen] SAY SHOW_PAGE " + list(_windowMain.listPages.keys())[_here] + " (" + str(_here) + ") # " + _windowMain.toShow["comment"])
			except: print("[Silverscreen] SAY SHOW_PAGE " + list(_windowMain.listPages.keys())[_here] + " (" + str(_here) + ")")
		
		for _body in _windowMain.toShow["bodies"]:
			if _body[0] == "b":
				_picture = pyglet.image.load(os.getcwd() + (os.name == 'nt' and '\\' or '/') + _body[1])
				_picture.blit(0, 0, 0, _windowMain.width, _windowMain.height)
			elif _body[0] == "h":
				_picture = pyglet.image.load(os.getcwd() + (os.name == 'nt' and '\\' or '/') + _body[1])
				_picture = _picture.get_region(0, _windowMain.height - int(_span1 * 2), _picture.width, int(_span1 * 2))
				_picture.blit(0, _windowMain.height - int(_span1 * 2), 0, _windowMain.width, _span1 * 2)
			else:
				_garo = int(_body[0]) % 3
				_x = 0
				if _garo == 2:
					_garo = "right"
					_x = _windowMain.width
				elif _garo == 1:
					_garo = "center"
					_x = _windowMain.width / 2
				else:
					_garo = "left"
				
				_sero = int(_body[0])
				_y = _windowMain.height
				if _sero >= 6:
					_sero = "bottom"
					_y = (_span1 * 2) - _windowMain.height
				elif _sero >= 3:
					_sero = "center2"
					_y = _windowMain.height / 2
				else:
					_sero = "top"
				
				try:
					_artifact = M2Label()
					_artifact.x(_x).y(_y).widthBox(_windowMain.width).heightBox(_windowMain.height).alignX(_garo).alignY(_sero)
					#_artifact.widthBox(_windowMain.width).heightBox(_windowMain.height)
					_artifact.text('<p align="' + _garo + '" valign="' + _sero + '"><font face="' + _fontDefault + '" size="' + str(_span1) + '">' + str(_body[1]) + '</font></p>')
					_artifact.decode().draw()
				except:
					print("[Silverscreen] ERROR Failed to render page " + str(_here))
					raise Exception
	else:
		print("[Silverscreen] WARNING " + _type0 + " is marked as deprecated. Use p2 instead")
		_title = str(title); _body = str(body)
		if _windowMain.inputStacked == '':
			try: print("[Silverscreen] SAY SHOW_PAGE " + list(_windowMain.listPages.keys())[_here] + " (" + str(_here) + ") # " + _windowMain.toShow["comment"])
			except: print("[Silverscreen] SAY SHOW_PAGE " + list(_windowMain.listPages.keys())[_here] + " (" + str(_here) + ")")
		
		# Background
		try:
			_picture = pyglet.image.load(os.getcwd() + (os.name == 'nt' and '\\' or '/') + background)
			if _type0 != 'lyrics':
				_picture = _picture.get_region(0, _windowMain.height - int(_span1 * 2), _picture.width, int(_span1 * 2))
				_picture.blit(0, _windowMain.height - int(_span1 * 2), 0, _windowMain.width, _span1 * 2)
			else: _picture.blit(0, 0, 0, _windowMain.width, _windowMain.height)
		except: print('[Silverscreen] SAY NO_SUCH_BACKGROUND')
		
		# Title
		try:
			_artifact = M2Label().x(_span1 / 4).y(_windowMain.height - (_span1 / 2)).widthBox(_windowMain.width).heightBox(_span1).alignX("left").alignY("center")
			_artifact.text('<font face="' + _fontDefault + '" size="' + str(_span1) + '" color="#ffffff">' + _title + '</font>')
			_artifact.decode().draw()
		except:
			traceback.print_exc()
			print('[Silverscreen] SAY NO_TITLE')
		
		# Body
		try:
			if _type0 == 'cover':
				_artifact = M2Label()
				_artifact.x(0).y((_windowMain.height / 2) - _span1).widthBox(_windowMain.width).heightBox(_windowMain.height - (_span1 * 2)).alignX("left").alignY("center2")
				_artifact.text('<p align="center"><font face="' + _fontDefault + '" size="' + str(_span1) + '">' + _body + '</font></p>')
				_artifact.decode().draw()
			else:
				_artifact = M2Label()
				_artifact.x(_span1 / 4).y(_windowMain.height - (_span1 * 2)).widthBox(_windowMain.width).heightBox(_span1).alignX("left").alignY("top")
				_artifact.text('<font face="' + _fontDefault + '" size="' + str(_span1) + '">' + _body + '</font>')
				_artifact.decode().draw()
		except: raise Exception
			

# Triggers
def on_draw():
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
		font_name = "' + _fontDefault + '", font_size = 36,
		x = _windowMain.width // 2, y = _windowMain.height // 2,
		anchor_x = 'center', anchor_y = 'center',
	).draw()
	'''
_windowMain.event(on_draw)

def on_key_press(value, modifiers):
	# Force use global ones about these
	global _path
	global _sheet
	global _here
	
	# Just for debugging
	#print('KEY ' + str(value) + ' (' + chr(value) + ')')
	#print('MOD ' + str(modifiers))
	
	if modifiers == 2: # With Ctrl
		if value == 114: # Ctrl + R: Reload the file
			_windowMain.nEscPressed = 0
			_hereRemember = _here
			_sheet = load_sheet(_path)
			if 'standard' in _sheet: _windowMain.standard = _sheet['standard']
			if 'pages' not in _sheet: raise Exception('No pages to show')
			_windowMain.listPages = _sheet['pages']
			_here = _hereRemember
		elif value >= 48 and value <= 57: # Ctrl + (Number): Key page (Number)
			#print("SAY key " + str(value))
			_keyPage = _windowMain.listKeyPages[value - 48]
			if _keyPage is not None:
				_windowMain.nEscPressed = 0
				_order = _keyPage
				_here = list(_windowMain.listPages.keys()).index(_order)
				_windowMain.toShow = list(_windowMain.listPages.values())[_here]
		_windowMain.inputStacked = ''
		_windowMain.nEscPressed = 0
	elif value >= 48 and value <= 57: # Number
		_windowMain.nEscPressed = 0
		if value != None: _windowMain.inputStacked += chr(value)
	elif value >= 97 and value <= 122: # Alphabet
		_windowMain.nEscPressed = 0
		if value != None: _windowMain.inputStacked += chr(value)
	elif value == 65293: # Enter: Send the order
		_windowMain.nEscPressed = 0
		_order = _windowMain.inputStacked
		#if _windowMain.inputStacked != None: print('ORDER ' +  _windowMain.inputStacked)
		if _order in _windowMain.listPages:
			_here = list(_windowMain.listPages.keys()).index(_order)
		else:
			_here1 = -1
			try: _here1 = int(_order) - 1
			except: _here1 = -1
			
			#print('LOAD_PAGE ' + list(_windowMain.listPages.keys())[_here1])
			if _here1 >= 0 and _here1 < len(_windowMain.listPages): _here = _here1
			else: print('[Silverscreen] SAY NO_SUCH_ORDER ' + _order)
			
		if _here != -1:
			#print('PAGE ' + str(_here))
			_windowMain.toShow = list(_windowMain.listPages.values())[_here]
		_windowMain.inputStacked = ''
	elif value == 65307: # Escape: Cancel the order
		_windowMain.inputStacked = ''
		if _windowMain.nEscPressed >= 2: None
		else:
			_windowMain.nEscPressed += 1
			#print('SAY ESC pressed ' + str(_windowMain.nEscPressed) + ' time(s)')
			return pyglet.event.EVENT_HANDLED
	elif value == 65361: # Left arrow: Previous page
		_windowMain.nEscPressed = 0
		_here -= 1
		if _here < 0: _here = 0
		_windowMain.toShow = list(_windowMain.listPages.values())[_here]
	elif value == 65363: # Right arrow: Next page
		_windowMain.nEscPressed = 0
		_here += 1
		if _here >= len(_windowMain.listPages): _here = len(_windowMain.listPages) - 1
		_windowMain.toShow = list(_windowMain.listPages.values())[_here]
	elif value == 65360: # Home: First page
		_windowMain.nEscPressed = 0
		_here = 0
		_windowMain.toShow = list(_windowMain.listPages.values())[_here]
	elif value == 65367: # End: Last page
		_windowMain.nEscPressed = 0
		_here = len(_windowMain.listPages) - 1
		_windowMain.toShow = list(_windowMain.listPages.values())[_here]
	elif value == 65474: # F5: Fullscreen ON/OFF
		_windowMain.nEscPressed = 0
		_windowMain.set_fullscreen(_windowMain.fullscreen == False)
	else:
		_windowMain.nEscPressed = 0
		#print('KEY ' + str(value) + ' (' + chr(value) + ')')
_windowMain.event(on_key_press)


# Go!
pyglet.app.run()
