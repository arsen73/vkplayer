#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, curses
from core.player import PlayerVK 

from core.parser import ParserVks

login = raw_input('Login:')
passw = raw_input('Password:')

def get_param(prompt_string):
     screen.clear()
     screen.border(0)
     screen.addstr(2, 2, prompt_string)
     screen.refresh()
     input = screen.getstr(10, 10, 60)
     return input



parser = ParserVks(login, passw)
#parser.SavePlayList(q)
#print('PLAY')
player = PlayerVK()
x = 0
while x != ord('4'):
	try:
		screen = curses.initscr()
		screen.clear()
		screen.border(0)
		screen.addstr(2, 2, "Please enter a number...")
		screen.addstr(4, 4, "1 - New Search")
		screen.addstr(5, 4, "2 - Pause")
		screen.addstr(6, 4, "3 - UnPause")
		screen.addstr(7, 4, "4 - Exit")
		screen.refresh()
		x = screen.getch()
		if x == ord('1'):
		    sw = get_param("Enter the word")
		    curses.endwin()
		    parser.SavePlayList(sw)
		    if(player.is_play):
		    	player.stop_play()
		    	player.setDefaultValue()
		    	player.kill = False
		    	player.start_play()
		    else:
		    	player.start()
		if x == ord('2'):
			player.pause_play()
		if x == ord('3'):
			player.unpaus_play()
	except KeyboardInterrupt:
		continue
player.stop_play()
curses.endwin()