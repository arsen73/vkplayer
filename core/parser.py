#!/usr/bin/python
# -*- coding: utf-8 -*-
import re, collections, sys, locale, os
from core.vkontakte import Vkontakte 
from pysqlite2 import dbapi2 as sqlite

class VkExeption(Exception):
	"""exeption for Vk parser"""
	def __init__(self, value):
		self.value = value

	def __str__(self):
		if self.value == 1:
			return 'authorization error'
		if self.value == 2:
			return 'nothing found'
		

class ParserVks(Vkontakte, VkExeption):
	""" get list audio from search page and save in db """
	def __init__(self, login, password):
		reload(sys)
		sys.setdefaultencoding('utf-8')
		Vkontakte.__init__(self,login, password)

	def listUrlAudio(self, sw):
		""" get audio list (href, performer, title) """
		if not self.testAuth():
			raise VkExeption(1)
		url = 'http://vk.com/search?c[q]='+sw+'&c[section]=audio&c[performer]=1'
		page = self.HtmlPage(url)
		sr = re.findall(r'<div class="play_btn_wrap".*?>(.+?)<span class="user"',page, re.DOTALL|re.MULTILINE)
		print len(sr)
		if len(sr) == 0:
			raise VkExeption(2)
		soundlist = []
		for s in sr:
			href = re.findall('(http://.*.mp3)', s)
			tit = re.findall(r'<span class="match".*?>(.+?)</span>', s, re.DOTALL|re.MULTILINE)
			title = re.findall(r'<a href="#".*?>(.+?)</a>', s, re.DOTALL|re.MULTILINE)
			sound = collections.namedtuple("sound", "href performer title")
			if len(href)>0:
				#print href
				sound.href = href[0]
			else:
				print sr
				break
			if len(tit)>0:
				#print tit[0]
				sound.performer = tit[0]
			#print s
			if len(title)>0:
				#print title[0]
				sound.title = title[0]
			soundlist.append(sound)

		return soundlist
		#return re.findall('(http://.*.mp3),', page)

	def CreateAudioPlaylist(self, q, file='playlist.m3u'):
		""" create m3u play list """
		urls = self.listUrlAudio(q)
		file = open(file, 'w')
		file.write('#EXTM3U\n')
		file.write('#EXTVLCOPT:network-caching=1000\n')
		#print(len(urls))
		#sys.stdout.write('@')
		for url in urls:
			file.write('#EXTINF:123,'+url.performer.encode('utf8')+' - '+url.title.encode('utf8')+ '\n')
			file.write(url.href+ '\n')

	def SavePlayList(self, q):
		""" search and save list audio in db """
		urls = self.listUrlAudio(q)
		con = sqlite.connect('users.db')
		cur = con.cursor()
		cur.execute('CREATE TABLE IF NOT EXISTS track (id INTEGER PRIMARY KEY, performer VARCHAR(100), title VARCHAR(100), url VARCHAR(512))')
		con.commit()
		cur.execute('DELETE FROM track WHERE 1')
		con.commit()
		for url in urls:
			#print url.title.decode('cp1251')
			#print url.href
			q = 'INSERT INTO track (id, performer, title, url) VALUES(NULL, "'+url.title.decode('cp1251')+'", "'+url.performer.decode('cp1251')+'", "'+url.href+'")'
			r1 = re.compile(r'<.*?>')
			q = r1.sub('', q)
			#print q
			cur.execute(q)
			#print(url.href)
			sys.stdout.write('@')
		con.commit()
		con.close()