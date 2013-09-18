#!/usr/bin/python
import urllib, urllib2
#import lxml.html
import re

class Vkontakte:
	def __init__(self, login, password):
		self.login = login
		self.password = password
		self.cookies = None

	def __ip_h(self):
		
		headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0'}
		req = urllib2.Request('http://vk.com/', None, headers)
		response = urllib2.urlopen(req)
		ip_h = re.findall(r'value="[a-z 0-9]{18}"', response.read())[0]

		return ip_h

	def __remixsid(self, ip_h):
		headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0'}

		values = {'act': 'login', 
		  		'q': '1',
		  		'al_frame': '1',
		  		'expire': '',
		  		'captcha_sid': '',
		  		'captcha_key': '',
		  		'from_host': 'vk.com',
		  		'from_protocol': 'http',
		  		'ip_h': ip_h,
		  		'email': self.login,
		  		'pass': self.password}

		data = urllib.urlencode(values)
		req = urllib2.Request('https://login.vk.com/?act=login', data, headers)
		response = urllib2.urlopen(req)

		return re.findall(r"remixsid=([a-z 0-9]*);", response.headers['Set-Cookie'])[0]

	def getCookies(self):
		if self.cookies: return self.cookies

		ip_h = self.__ip_h()
		remixsid = self.__remixsid(ip_h)

		list_cookies = ['remixlang=0;', 
		                'remixchk=5;',
		                'remixdt=0;', 
		                'audio_vol=55;',
		                'remixflash=11.2.202;',
		                'remixseenads=2;'
		                'remixsid=' + remixsid + ';',
		                'remixreg_sid=;',
		                'remixrec_sid=']

		return " ".join(list_cookies);

	def HtmlPage(self, url):
		cookie = self.getCookies()

		header = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0',
					'Cookie': cookie}

		req = urllib2.Request(url, None, header)
		response = urllib2.urlopen(req)

		return response.read()
