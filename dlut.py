#coding=utf-8

import urllib
import re
import sys
import time
import signal
from bs4 import BeautifulSoup

def signalHandler(signalNum,frame):
    print 'EXIT'
    exit(0)

#注册退出信号
signal.signal(signal.SIGINT,signalHandler)

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()

    return html

def getLastAndNext(html):
    lastRe = 'a href.*?[0-9].*? class="Prev'
    la = re.compile(lastRe)
    nextRe = 'href.*?[0-9].*? class="Next'
    ne = re.compile(nextRe)


    try:
        lastPage = re.findall(la,html)[0]
        print 'pre'
        print re.findall(la,html)
        lastPage = lastPage.split('"')[-3]
        try:
            lastPage = lastPage.split('/')[1]
        except Exception:
            pass
    except Exception:
        lastPage = ''
    try:
        nextPage = re.findall(ne,html)[0]
        print 'next'
        print re.findall(ne,html)
        nextPage = nextPage.split('"')[-3]
        try:
            nextPage = nextPage.split('/')[1]
        except Exception:
            pass
    except Exception:
        nextPage = ''

    page = 'http://ssdut.dlut.edu.cn/index/bkstz/'
    print 'lastpageurl',lastPage
    print 'nextpageurl',nextPage
    if lastPage != '':
        lastPage = page + lastPage
    if nextPage != '':
        nextPage = page + nextPage

    print lastPage,nextPage
    return lastPage,nextPage


def getMesList(html):
    mesRe = r'<a href=".*?.htm" class="c566.*?>'
    mes = re.compile(mesRe)
    titles = re.findall(mes,html)

    titleDisk = {}
    titleUrlDisk = {}
    i = 0 
    for t in titles:
        tempT = t.split('"')[7]
        tempUrl = t.split('"')[1]
        titleDisk[i] = tempT
        titleUrlDisk[tempT] = tempUrl

        i += 1

    lastPage,nextPage = getLastAndNext(html)

    return titleDisk,titleUrlDisk,lastPage,nextPage


#获取具体信息
def getExactlMes(html):
    #正则式.*不能匹配换行[\s\S]可以
    mesRe = r'<h1 ali[\s\S]*<p align'
    mes = re.compile(mesRe)
    exactlMes = re.findall(mes,html)

    beautifulSoup = BeautifulSoup(exactlMes[0])
    realMes = beautifulSoup.findAll('p')
    for s in realMes:
        print s.text


def readMes(titleDisk,titleUrlDisk,titleNum):
    try:
        print titleUrlDisk[titleDisk[titleNum]]
        titleUrl = titleUrlDisk[titleDisk[titleNum]]
    except Exception:
        return
    titleUrl = titleUrl.split('..')[-1]
    titleUrl = 'http://ssdut.dlut.edu.cn' + titleUrl

    print titleUrl
    html = getHtml(titleUrl)

    getExactlMes(html)

    print '退出当前页:r'


def showMes(titleDisk,titleUrlDisk,lP,nP,curUrl):
    #学生周知的首页地址
    firstUrl = 'http://ssdut.dlut.edu.cn/index/bkstz.htm'

    for i in range(len(titleDisk)):
        print '%d : %s' % (i,titleDisk[i])


    print '\n选择对应序号读取具体内容\n'
    print '上一页:l',lP
    print '下一页:n',nP
    print '刷新:r'
    print '退出:q | ctrl+c'

    while True:
        #raw_input() 从控制台读入一个数字
        inNum = raw_input()

        if inNum == 'l':
            print lP
            if lP != '':
                start(lP,lP)
            else:
                start(firstUrl,firstUrl)
        elif inNum == 'n':
            print 'np',nP
            if nP != '':
                start(nP,nP)
        elif inNum == 'r':
            start(curUrl,curUrl)
        elif inNum == 'q':
            exit(0)


        try:
            titleNum = int(inNum)
        except Exception:
            continue


        readMes(titleDisk,titleUrlDisk,titleNum)

#参数：将要打开的url，当前的url
def start(url,curUrl):
    print '正在加载......'
    html = getHtml(url)
    titleDist,titleUrlDisk,lP,nP = getMesList(html)
    showMes(titleDist,titleUrlDisk,lP,nP,curUrl)

def welcome():
    print '欢迎使用学生周知之控制台版'
    time.sleep(1)

    url = 'http://ssdut.dlut.edu.cn/index/bkstz.htm'
    start(url,url)

welcome()
