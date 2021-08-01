Silverscreen.py - A lightweight presentation app

Version 0.0.5

Copyright (C) 2018-2021 Minho Jo <whitestone8214@gmail.com>

License: GNU General Public License version 3 (or any later version) (see license.txt)

Required:
	- Python (Tested on 3.9.0)
	- Modified Pyglet ( git clone https://github.com/whitestone8214/pyglet-1.4.10-mod )
		- Extract pyglet from pyglet-1.4.10-mod after clone ( mv pyglet-1.4.10-mod/pyglet . )
		- Original Pyglet ( https://github.com/pyglet/pyglet ) might work, but it has some limitations (i.e. font size, vertical layout, etc.)
	- Modified PyJSON5 ( git clone https://github.com/whitestone8214/pyjson5-0.8.5-mod )
		- Extract json5 from pyjson5-0.8.5-mod after clone ( mv pyjson5-0.8.5-mod/json5 . )

Usage:
	- silverscreen.py [options] [sheet file]
		- -screen=SCREEN: Set base screen as SCREEN
		- -width=WIDTH: Set window width as WIDTH
		- -height=HEIGHT: Set window height as HEIGHT
		- -x=X: Set window's horizontal position as X
		- -y=Y: Set window's vertical position as Y
		- -frameless: Set window without title bar
	
Keys:
	- Esc: Exit (Press 3 times continuously; Other keys will reset the count)
	- F5: Fullscreen ON/OFF
	- Ctrl + R: Reload
	- 123 -> Enter: Go to 123rd slide
	- name -> Enter: Go to slide named 'name'
	- Ctrl + (Number): Go to key page (Number) (If defined)
	- Left arrow: Go to previous page
	- Right arrow: Go to next page
	- Home: Go to the first page
	- End: Go to the last page
	
Example:
	- ./silverscreen.py example.j5
