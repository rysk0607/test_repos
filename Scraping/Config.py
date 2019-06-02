#!/usr/bin/env python
# coding: utf-8
#
#漫画天国について設定内容を記載
#
import datetime
import os

class Config:
    def __init__(self):
        self.className   = 'Config'

        self.HOMEDIR = os.getcwd()
        self.DATADIR =self.HOMEDIR + '\\data'
        self.IMGDIR  =self.DATADIR + '\\image'
        

    #引数のメッセージを出力（※引数に\nを含めると改行）
    def echoMsg(self, msg):
        print '#####################################'
        print datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        print msg
        print '#####################################'


if __name__ == '__main__':
    c = Config()
    c.echoMsg("test")
    
