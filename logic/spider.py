# -*-encoding:utf-8 -*-
import urllib2
import urllib
import cookielib
import base64
import chardet

#实现登录cookie
useragent = "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"
url = "http://poj.org/login"
postdata = urllib.urlencode({
    "user_id1":"STUDENTOJ",
    "password1":"STUDENTOJ"
}).encode('utf-8')
headers = ("User-Agent", useragent)
req = urllib2.Request(url, postdata)
req.add_header('User-Agent', useragent)
cjar = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cjar))
urllib2.install_opener(opener)
data = opener.open(req).read()
fhandle = open("F:\\biyesheji\\gradu_pro\\base_version\spider_content\\1poj_login.html",'wb')
fhandle.write(data)
fhandle.close()

#获取题目内容
url2 = "http://poj.org/problem?id="  #http://poj.org/problem?id=1001&lang=zh-CN
pro_id = "1001"
req2 = urllib2.Request(url2+pro_id+'&lang=zh-CN')
req2.add_header('User-Agent', useragent)
data2 = urllib2.urlopen(req2).read()
fhandle2 = open("F:\\biyesheji\\gradu_pro\\base_version\spider_content\\2problem_content.html",'wb')
fhandle2.write(data2)
fhandle2.close()

#提交代码
url3 = "http://poj.org/submit?problem_id="
pro_id = "1001"
with open('F:\\biyesheji\Untitled1.cpp','r')as f:
    code = f.read()
print chardet.detect(code)
code = code.decode('GB2312').encode('utf-8')
code = str(base64.b64encode(code))
# print code
postdata2 = urllib.urlencode({
    "problem_id":"1001",
    "language":"4", #0:G++ 1:gcc;2:java;3:pascal;4:C++;5:C;6:Fortran
    "source":code,
    "submit":"Submit",
    "encoded":"1"
}).encode('utf-8')
req3 = urllib2.Request(url3+pro_id, postdata2)
req3.add_header('User-Agent', useragent)
data3 = urllib2.urlopen(req3).read()
fhandle3 = open("F:\\biyesheji\\gradu_pro\\base_version\spider_content\\3submit_result.html",'wb')
fhandle3.write(data3)
fhandle3.close()


#返回提交的结果
url4 = "http://poj.org/status?problem_id=1001&user_id=STUDENTOJ&result=&language="
req4 = urllib2.Request(url4)
req4.add_header('User-Agent', useragent)
data4 = urllib2.urlopen(req4).read()
fhandle4 = open("F:\\biyesheji\\gradu_pro\\base_version\spider_content\\4compile_result.html", "wb")
fhandle4.write(data4)
fhandle4.close()
