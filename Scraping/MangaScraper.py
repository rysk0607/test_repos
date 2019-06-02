#!/usr/bin/env python
# coding: utf-8

#
#株価データをスクレイピングにより取得する
#
#2019/04/30 yonezawa-ry
#
#コーディング命名規則として、キャメルケースを使用すること
#
#漫画天国より情報取得
#http://mangadld.com/?p=140  1150
#
#実際の取得は下記のように銘柄コード、年度を伴うURLから行う
#https://kabuoji3.com/stock/3436/2018/
#株価のテーブルには、下記のクラスが設定されている。
#


import urllib
from BeautifulSoup import *
import time
import re
import sys
import os
import datetime
import csv

#自作クラス
import Config
import Content

class MangaScraper:
    #コンストラクタ
    def __init__(self):
        self.className   = 'MangaScraper'

        self.cfg         = Config.Config()        

        self.baseURL     = 'http://mangadld.com/?p='
        self.sleepSec    = 0.01 #[sec]

        self.contents    = [] #Contentを入れ込む

        #debug用
        self.soup = None
        


    #入力されたurlに対して、パースされたオブジェクトを返す
    def getSoup(self, url):
        html = urllib.urlopen(url)
        return BeautifulSoup(html.read())
        
    def sleep(self):
        time.sleep(self.sleepSec)


    #tdについて検索
    #listで返す
    def getTds(self, soup):
        return soup.findAll("td")

    def shaveTag(self, s):
        m = re.search('<.+>(.+?)<.+>',s)
        if m:
            return m.group(1)
        else:
            return None

    #pageのtitleタグを取得する
    #strでタイトルの中身を返す
    def getTitle(self, soup):
        return soup.find("title").text

    #pageからtableタグを検索し取得する
    #単一soupクラスで返す
    def getTable(self, soup):
        return soup.find("table")

    #pageからaタグを検索し取得する
    #単一aタグクラスで返す
    def getA(self, soup):
        return soup.find("a")

    
    #pageからtrタグを検索し取得する
    #リストのsoupクラスで返す
    def getTrs(self, soup):
        return soup.findAll("tr")

    #pageからsectionタグを検索し取得する
    #単一sectionタグクラスで返す
    def getSection(self, soup):
        return soup.find("section")

    #pageからimageタグを検索し取得する
    #単一imageタグクラスで返す
    def getImg(self, soup):
        return soup.find("img")

    #pageからimageタグを検索し取得する
    #複数imageタグクラスリストで返す
    def getImgs(self, soup):
        return soup.findAll("img")
    

    #aタグオブジェクトからURLを取得する
    #URLの文字列で返す
    def getUrlFromAtag(self, atag):
        m = re.search('.+href\="(htt.+?)".+', str(atag) )
        if m:
            return m.group(1)
        else:
            return None

    #imgタグオブジェクトから画像URLを取得する
    #URLの文字列で返す
    def getImgUrlFromImgTag(self, imgTag):
        
        m = re.search('.+src\="(h.+?)".+', str(imgTag) )
        if m:
            return m.group(1)
        else:
            return None 
        

    #メインプロセス
    #指定されたコードについて情報取得
    def process(self, code=140):
        #準備
        #self.sleep()        

        url = self.baseURL + str(code)
        #url = self.baseURL  #DEBUG用
        
        soup = self.getSoup(url)
        self.soup = soup

        table  = self.getTable(soup)
        if table != None:
            #データがありそうな場合、データ抽出を行う。
            c       = Content.Content()        
            c.TITLE = self.getTitle(soup)
            c.CODE  = str(code)
            self.cfg.echoMsg(c.CODE + ' : ' +  c.TITLE)        
            #c.CODE = str(111)
            #IMAGEを取得する
            #完全解剖できていないが、暫定的に[2]を指定する。（[0]はロゴ、[1]はアイキャッチ）
            c.IMGURL = self.getImgUrlFromImgTag(self.getImgs( soup )[2] )            
            trs    = self.getTrs(table)
            for i,tr in enumerate(trs):
                atag = self.getA(tr)
                if atag != None:
                    c.appendData( [atag.text, self.getUrlFromAtag(atag)] )
            #データ出力
            if c.putData(self.cfg.DATADIR) < 1:
                #CSV出力成功した場合、併せて画像取得も行う。
                urllib.urlretrieve(c.IMGURL , self.cfg.IMGDIR + "\\" + str(code) + ".jpg" )
                print 'SUCCESS'
            else:
                print 'FAILED'                
            self.contents.append(c)

            

if __name__ == '__main__':
    #class生成
    c = MangaScraper()

    #開始メッセージ
    c.cfg.echoMsg('START')

    #メインプロセス
    #指定コードの情報取得・出力
    M = 1300
    m = 1
    for i in range(M - m):
        c.process(i + m)

    #終了メッセージ
    c.cfg.echoMsg('END')

