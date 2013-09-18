#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, threading
from PyQt4 import QtGui, QtCore
from core.player import PlayerVK 
from core.parser import ParserVks
from core.parser import VkExeption

class MainWindow(QtGui.QWidget, threading.Thread):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)

		self.resize(350, 250)
		self.setWindowTitle('Player')
		self.setWindowIcon(QtGui.QIcon('vk.ico'))

		self.slider = QtGui.QSlider(QtCore.Qt.Vertical, self)
		#option = QtGui.QStyleOptionSlider()
		#option.sliderValue = 50
		#option.sliderPosition = 50
		#self.slider.initStyleOption(option)

		styles = """
		QTextEdit {
		font: bold 16pt Monotype Corsiva;
		color: white;
		background-color: black;
		selection-color: black;
		selection-background-color: white;
		}
		"""



		self.slider.setTickPosition(50)
		self.list = QtGui.QListWidget()
		self.prev_button = QtGui.QPushButton('Prev')
		self.next_button = QtGui.QPushButton('Next')
		self.play_button = QtGui.QPushButton('Play')
		self.stop_button = QtGui.QPushButton('Stop')

		self.stop_button.setStyleSheet(styles)

		self.search_button = QtGui.QPushButton('Search')
		self.label = QtGui.QLabel('')

		login, ok = QtGui.QInputDialog.getText(self, 'Login', 'Login:')
		if ok:
			login = unicode(login)
		else:
			sys.exit()
		passw, ok = QtGui.QInputDialog.getText(self, 'Password', 'Password:',  QtGui.QLineEdit.Password)
		if ok:
			passw = unicode(passw)
		else:
			sys.exit()

		self.parser = ParserVks(login, passw)
		self.player = PlayerVK()
		self.play_list = {}
		self.first_start = True

		grid = QtGui.QGridLayout()

		#размещаю по сетке
		grid.addWidget(self.search_button, 2, 5)
		grid.addWidget(self.slider, 0, 5, 1, 5)
		grid.addWidget(self.list, 0, 0, 1, 4)     
		grid.addWidget(self.prev_button, 2, 0)
		grid.addWidget(self.stop_button, 2, 1)
		grid.addWidget(self.play_button, 2, 2)
		grid.addWidget(self.next_button, 2, 3)
		grid.addWidget(self.label, 3, 0, 3, 5)

		#добавляем события
		self.connect(self.slider, QtCore.SIGNAL('valueChanged(int)'), self.volumeSet)

		self.connect(self.list, QtCore.SIGNAL('currentRowChanged(int)'), self.playStart)

		self.connect(self.prev_button, QtCore.SIGNAL('clicked()'), self.prevItem)
		self.connect(self.next_button, QtCore.SIGNAL('clicked()'), self.nextItem)

		self.connect(self.play_button, QtCore.SIGNAL('clicked()'), self.UnPause)
		self.connect(self.stop_button, QtCore.SIGNAL('clicked()'), self.Pause)

		self.connect(self.search_button, QtCore.SIGNAL('clicked()'), self.showDialogSearch)

		self.connect(self, QtCore.SIGNAL('close()'), self.__del__)


		self.setLayout(grid)
		self.getPlayList()
		self.list.setCurrentRow(0)


	def showDialogSearch(self):
		text, ok = QtGui.QInputDialog.getText(self, 'Search', 'Enter text:')
		if ok:
			self.label.setText(unicode(text))
			self.Search(unicode(text))

	def getPlayList(self):
		self.list.clear()
		self.play_list = self.player.getPlayList()
		for item in self.play_list:
			self.list.insertItem(item[0], item[1]+'-'+item[2])
		self.list.setCurrentRow(0)

	def nextItem(self):
		lenght_list = self.list.count()
		activ_iem = self.list.currentRow()
		if lenght_list-1 == activ_iem:
			activ_iem = -1
		next_activ = activ_iem + 1
		self.list.setCurrentRow(next_activ)

	def prevItem(self):
		lenght_list = self.list.count()
		activ_iem = self.list.currentRow()
		if 0 == activ_iem:
			activ_iem = lenght_list
		prev_activ = activ_iem - 1
		self.list.setCurrentRow(prev_activ)

	def playStart(self):
		activ_iem = self.list.currentRow()
		print activ_iem
		if self.player.getIsInit():
			self.player.kill = True
			self.player.stop_play()
			self.player = PlayerVK()
		self.player.setDefaultValue()
		self.player.kill = False
		self.player.set_item(self.play_list[activ_iem])
		self.player.start()


	def Pause(self):
		print "Pause Play"
		self.player.pause_play()

	def UnPause(self):
		print "UnPause Play"
		self.player.unpaus_play()

	def Search(self, sw):
		print "Search"
		try:
			self.parser.SavePlayList(sw)
		except VkExeption as e:
			self.label.setText(unicode(e))
			return
		self.getPlayList()
		self.playStart()

	def volumeSet(self):
		pv = self.slider.value()
		self.player.setVolume(pv)

	def __del__(self):
		print "exit"
		if(self.player.getIsInit()):
			self.player.kill = True
			self.player.stop_play()