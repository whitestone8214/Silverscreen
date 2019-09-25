Silverscreen.py - A lightweight presentation app

Version 0.0.2

Copyright (C) 2018-2019 Minho Jo <whitestone8214@gmail.com>

License: GNU General Public License version 3 (or any later version) (see license.txt)

Required:
	- Python 3.x (Tested on 3.7.0; 2.x are not supported)
	- Modified Pyglet ( git clone https://github.com/whitestone8214/pyglet-1.3.0-mod pyglet )
		- Original Pyglet ( https://bitbucket.org/pyglet/pyglet/overview ) might work, but it has some limitations (i.e. font size, vertical layout, etc.)
	- pyjson5 ( git clone https://github.com/dpranke/pyjson5 )

Usage:
	- silverscreen.py [sheet file]

Option:
	(not yet)
	
Keys:
	- Esc: Exit
	- F5: Fullscreen ON/OFF
	- Ctrl + R: Reload
	- 123 -> Enter: Go to 123rd slide
	- name -> Enter: Go to slide named 'name'
	- Left arrow: Go to previous page
	- Right arrow: Go to next page
	- Home: Go to the first page
	- End: Go to the last page
	
Example:
	- ./silverscreen.py example.j5
