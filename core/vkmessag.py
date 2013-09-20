#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib, lxml.html, collections, urllib2
from vkontakte import Vkontakte

class Vkmessag(Vkontakte):
	"""docstring for Vkmessag"""

	def getListDialog(self):
		url_mail = "http://m.vk.com/mail"
		self.testAuth() #проверяем авторизацию
		html = self.HtmlPage(url_mail) #получаем страницу списка диалогов
		doc = lxml.html.document_fromstring(html)
		i = 1
		self.listConverstetions = []
		Converstation = collections.namedtuple('Converstation', ['Id', 'Name', 'DateLast', 'href'])
		for converstetion in doc.cssselect('a.dialog_item'):
			name = converstetion.cssselect('span.mi_author')
			data = converstetion.cssselect('span.di_date')
			print str(i)+"\t"+name[0].text
			self.listConverstetions.append(Converstation(i, name[0].text, data[0].text, converstetion.get('href')))
			i +=1
			# выводим на экран названия топиков.

	def getListMessag(self, id = None, last_m = False):
		if id == None:
			print "Enter id converstetion"
		else:
			url_conv = "http://m.vk.com"+self.listConverstetions[int(id)-1].href
			html = self.HtmlPage(url_conv) #получаем страницу диалога
			doc = lxml.html.document_fromstring(html)
			list_msg = doc.cssselect('div.msg_item div.mi_text')
			#action для формы сообщения
			form = doc.cssselect('form')
			self.action_form = form[0].get('action')
			print self.action_form
			for m in list_msg:
				print m.text
				if last_m:
					return list_msg
			return list_msg

	def getMessag(self):
		pass

	def SendMessag(self, message):
		headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0'}

		values = {'message': str(message),
				'_ajax':1}
		data = urllib.urlencode(values)
		req = urllib2.Request("http://m.vk.com"+self.action_form, data, headers)
		response = urllib2.urlopen(req)
		print response


if __name__ == '__main__':
	print "test Vkmessag"
	ob = Vkmessag('+380684757116', 'niko2012')
	ob.getListDialog()
	idm = raw_input('Id: ')
	ob.getListMessag(idm)
	message = raw_input('Messag: ')
	ob.SendMessag(message)
