#!/usr/bin/python
# -*- coding: utf-8 -*-
from urllib import urlretrieve

class Dfile:
	def __init__(self):
		print('')

	def downloadFile(self, fileUrl, fileName):
		print "start download"
		urlretrieve(fileUrl, fileName + '.mp3')
		print "\n\r download:"

#downloadFile('http://cs9-6v4.vk.me/p18/6af41ebf04cf54.mp3', 'test')