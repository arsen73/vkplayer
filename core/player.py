#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame, threading, sys
from pysqlite2 import dbapi2 as sqlite
from download import Dfile


class PlayerVK(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.kill = False
        self.is_play = False

    def run(self):
        self.play_item()

#Попытаться проиграть
    def play_music(self, music_file):
        #Инициализируе часы.
        clock = pygame.time.Clock()
        try:
            #Загружае файл.
            pygame.mixer.music.load(music_file)
            print "Music file %s loaded!" % music_file
        except pygame.error:
            #Ловим ошибки загрузки
            print "File %s not found! (%s)" % (music_file, pygame.get_error())
            return
        #Проигрываем
        pygame.mixer.music.play()
        #Ожидаем завершение проигрывания
        while pygame.mixer.music.get_busy():
            #Запускаем задержку - разгрузить процессор.
            clock.tick(30)  

#проигрываем всё из таблицы
    def start_play(self, id = 0):
        #выбираем две записи
        self.con = sqlite.connect('users.db')
        cur = self.con.cursor()
        if id > 0:
            cur.execute('SELECT * FROM track WHERE id > '+str(id))
        else:
            cur.execute('SELECT * FROM track')
        res = cur.fetchall()
        self.con.close()
        for row in res:
            if(self.kill):
                return
            file_track = Dfile()
            file_track.downloadFile(row[3], '1')
            print(row[1]+'-'+row[2]+"\n\r")
            self.play_music('1.mp3')

    def set_item(self, item):
        self.item_activ = item

#проигрывает выбранную запись
    def play_item(self):
        if(self.kill):
            return
        file_track = Dfile()
        file_track.downloadFile(self.item_activ[3], '1')
        print(self.item_activ[1]+'-'+self.item_activ[2]+"\n\r")
        pygame.mixer.music.stop()
        self.play_music('1.mp3')
        self.start_play(self.item_activ[0])

#установка значений по умолчанию
    def setDefaultValue(self):
         #Устанавливаем параметры Микшера.
        freq = 44100     # audio CD quality
        bitsize = -16    # unsigned 16 bit
        channels = 2     # 1 is mono, 2 is stereo
        buffer = 2048    # number of samples (experiment to get right sound)
        #Инициализируем микшер.
        pygame.mixer.init(freq, bitsize, channels, buffer)

        #Устанавливаем грокость - 0.5.
        pygame.mixer.music.set_volume(0.5)

#устанавливаем громкость
    def setVolume(self, v):
        v = float(v)
        print v/100
        pygame.mixer.music.set_volume(v/100)

#пауза
    def pause_play(self):
        pygame.mixer.music.pause()

#старт
    def unpaus_play(self):
        pygame.mixer.music.unpause()

#остановка и переход к концу списка
    def stop_play(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.set_endevent()
        self.kill = True

#возвращает список
    def getPlayList(self):
        #выбираем записи
        self.con = sqlite.connect('users.db')
        cur = self.con.cursor()
        cur.execute('SELECT * FROM track')
        res = cur.fetchall()
        self.con.close()
        return res

    def getIsInit(self):
        if pygame.mixer.get_init() == None :
            return False
        return True

 #   def __del__(self):
        #pygame.mixer.music.fadeout(1000)
        #pygame.mixer.music.stop()
        #self.con.close()
        #sys.exit()