#-*-coding: utf-8 -*-

import re
import urllib2
import urllib
from bs4 import BeautifulSoup
#获取小标题
def get_title(soup):
    return soup.find_all(name='p', attrs={"class":"pst"})
#获取文本
def get_text(soup):
    return soup.find_all(name='div', attrs={"class":"ptx"})
#获取样例
def get_sample(soup):
    return soup.find_all(name='pre', attrs={"class":"sio"})

#解析题目内容
def analyse(url):
    useragent = "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
                "(KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"
    # url = 'http://poj.org/problem?id=1000'
    req = urllib2.Request(url)
    req.add_header('User-Agent', useragent)
    data = urllib2.urlopen(req).read()
    # print data
    soup = BeautifulSoup(data, 'html.parser')
    # print soup
    text_list = get_text(soup)[0:3]
    title_list = get_title(soup)[0:5]
    sample_list = get_sample(soup)
    text = list()
    title = list()
    all = list()
    # 处理文本 加换行符
    for i in text_list:
        text.append(i.text + '\r\n')
    for i in title_list:
        title.append("\r\n#### " + i.text + '\r\n')
    for i in sample_list:
        i = '```\r\n' + i.string + '\r\n' + '```\r\n'
        text.append(i)
    # print text
    for i in range(5):
        all.append(title[i] + text[i])
    URL = '[题目链接]' + '(' + url + ')' + '\r\n'
    f = open('F:\\biyesheji\gradu_pro\\base_version\spider_content\\POJ.txt', 'w')
    f.write(URL)
    for i in all:
        f.write(i)
    # f.write("#### AC\n- ")
    f.close()
    print("Done!")

url = 'http://poj.org/problem?id=1000'
analyse(url)
#
# useragent = "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"
# req = urllib2.Request(url)
# req.add_header('User-Agent', useragent)
# data = urllib2.urlopen(req).read()
# # print data
# soup = BeautifulSoup(data, 'html.parser')
# # print soup
#
# text_list = get_text(soup)[0:3]
# title_list = get_title(soup)[0:5]
# sample_list = get_sample(soup)
#
# text = list()
# title = list()
# all = list()
# #处理文本 加换行符
# for i in text_list:
#     text.append(i.text + '\r\n')
# for i in title_list:
#     title.append("#### " + i.text + '\r\n')
# for i in sample_list:
#     i = '```\r\n' + i.string + '\r\n' + '```\r\n'
#     text.append(i)
# print text
#
# for i in range(5):
#     all.append(title[i] + text[i])
# URL = '[题目链接]' + '(' + url + ')' + '\r\n'
# f = open('POJ.txt', 'w')
# f.write(URL)
# for i in all:
#     f.write(i)
# f.write("#### AC\n- ")
# f.close()
# print("Done!")
#
