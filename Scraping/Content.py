#!/usr/bin/env python
# coding: utf-8
#
#漫画天国について、取得用データの設定内容を記載
#

import csv

class Content:
    def __init__(self):
        self.className   = 'Content'
        self.TITLE  = None
        self.CODE   = None
        self.IMGURL = None

        #下記の順でデータを保有
        #[ [リンク名,リンクURL], [リンク名,リンクURL] ...]
        self.DATA = []


    #DATA出力
    #０：正常終了、１：タイトルなし、２：コードなし、３：データなし、９：例外
    def putData(self, dirPath):
        try:
            
            if self.TITLE == None:
                return 1
            if self.CODE == None:
                return 2
            if len(self.DATA) < 1:
                return 3
            csvFileName = dirPath + '\\' + self.CODE + '.csv'
            f = open(csvFileName,"w")
            w = csv.writer(f, lineterminator='\n')

            w.writerow( [self.CODE, self.TITLE, self.IMGURL] )

            for i,x in enumerate(self.DATA):
                w.writerow(x)
            f.close()
            return 0
        except:
            return 9
            
    #格納データにリストデータをappend
    def appendData(self, l):
        self.DATA.append(l)
    

if __name__ == '__main__':
    c = Content()
    print c.putData('aaa')
    
