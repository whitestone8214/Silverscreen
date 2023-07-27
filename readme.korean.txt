Silverscreen.py - 경량의 프레젠테이션 프로그램

Version 0.0.6

Copyright (C) 2018-2023 Minho Jo <whitestone8214@gmail.com>

License:
	silverscreen.py: GNU General Public License version 3 (이후 버전 적용 가능) (license.gpl3.txt 참고)
	side.py: MIT License (license.mit.txt 참고)

필요한 것:
	- Python (3.11.3에서 정상 동작을 확인했습니다)
	- 특별히 개조된 Pyglet ( git clone https://github.com/whitestone8214/pyglet-1.4.10-mod )
		- 클론 후 pyglet-1.4.10-mod/pyglet 의 심볼릭 링크를 만듭니다 ( ln -s pyglet-1.4.10-mod/pyglet . )
		- 원본 Pyglet ( https://github.com/pyglet/pyglet ) 의 경우 사용 가능은 하겠으나 폰트 크기, 수직 레이아웃 등 몇 가지 측면에서 제약이 있습니다.
	- 특별히 개조된 PyJSON5 ( git clone https://github.com/whitestone8214/pyjson5-0.8.5-mod )
		- 클론 후 pyjson5-0.8.5-mod/json5 의 심볼릭 링크를 만듭니다 ( ln -s pyjson5-0.8.5-mod/json5 . )
	
사용법:
	- silverscreen.py [옵션] [시트 파일]
		- -screen=A: A번 화면을 기준으로 합니다
		- -width=WIDTH: 창의 가로 크기를 WIDTH로 합니다
		- -height=HEIGHT: 창의 세로 크기를 HEIGHT로 합니다
		- -x=X: 창의 가로 위치를 X로 합니다
		- -y=Y: 창의 세로 위치를 Y로 합니다
		- -frameless: 창을 타이틀바가 없게 합니다
	
키:
	- Esc: 종료 (3회 연타 필요; 중간에 다른 키를 누르면 카운트 초기화)
	- F5: 전체 화면 ON/OFF
	- Ctrl + R: 다시 로드
	- 123 -> Enter: 123번째 슬라이드 표시
	- name -> Enter: 이름이 name인 슬라이드 표시
	- Ctrl + (숫자): (숫자)번 키페이지 표시 (지정되었을 경우)
	- 왼쪽 방향키: 이전 페이지로
	- 오른쪽 방향키: 다음 페이지로
	- Home: 첫 페이지로
	- End: 마지막 페이지로
	
예제:
	- ./silverscreen.py example.j5
