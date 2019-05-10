#-*-coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import time
import urllib2
import urllib
import cookielib
import re
import base64
import chardet
from flask import Blueprint,request,session,g,redirect,url_for,abort,render_template,flash
from werkzeug.security import check_password_hash,generate_password_hash
from database_op import get_db, connect_db
import functools
from login_and_register import login_required
from werkzeug.utils import secure_filename
import werkzeug

bp4 = Blueprint('spider', __name__, url_prefix='/spider')
useragent = "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"


@bp4.route('/spider_search',methods=['POST','GET'])
@login_required
def spider_search():
    if request.method == 'POST':
        pro_ojid = request.form['pro_ojid']
        oj_name = request.form['oj_name']
        pro_ojid = request.values.get('pro_ojid')
        # oj_name =
        # 实现登录cookie
        url = "http://poj.org/login"
        postdata = urllib.urlencode({
            "user_id1": "STUDENTOJ",
            "password1": "STUDENTOJ"
        }).encode('utf-8')
        req = urllib2.Request(url, postdata)
        req.add_header('User-Agent', useragent)
        cjar = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cjar))
        urllib2.install_opener(opener)
        data = opener.open(req).read()
        fhandle = open("F:\\biyesheji\\gradu_pro\\base_version\spider_content\\1poj_login.html", 'wb')
        fhandle.write(data)
        fhandle.close()
        # 获取题目内容
        url2 = "http://poj.org/problem?id="  # http://poj.org/problem?id=1001&lang=zh-CN
        req2 = urllib2.Request(url2 + pro_ojid)
        req2.add_header('User-Agent', useragent)
        data2 = urllib2.urlopen(req2).read()
        fhandle2 = open("F:\\biyesheji\\gradu_pro\\base_version\spider_content\\2problem_content.html", 'wb')
        fhandle2.write(data2)
        fhandle2.close()
        print '开始解析题目。。。'
        with open('F:\\biyesheji\gradu_pro\\base_version\spider_content\\2problem_content.html', 'r') as f:
            pro_content = f.read()
        pata = '<div class="ptt" lang="(zh-CN|en-US)">.+?</div>'
        presult1 = re.search(pata, pro_content, re.S)
        ptitle1 = pro_content[presult1.span()[0]:presult1.span()[1]]
        pataa = '>.+?<'
        presult2 = re.search(pataa, ptitle1)
        ptitle2 = ptitle1[presult2.span()[0]:presult2.span()[1]]
        title = ptitle2[1:-1]
        print title
        g.title = pro_ojid + '.' + title
        # g.describe = 'http://poj.org/problem?id=' + pro_ojid
        g.pro_ojid = pro_ojid
        # title解决
        from bs import analyse
        analyse(url2 + pro_ojid)
        with open('F:\\biyesheji\gradu_pro\\base_version\spider_content\POJ.txt','r') as poj:
            g.describe = poj.readlines()
        return render_template('/spider/spider_submit.html')
    return render_template('/spider/search.html')


@bp4.route('/spider_submit',methods=['GET','POST'])
@login_required
def spider_submit():
    pro_ojid = request.args.get("pro_ojid")
    code = request.form['code']
    lan = request.form['language']
    #提交代码
    url3 = "http://poj.org/submit?problem_id="
    code = code.encode('utf-8')
    code = str(base64.b64encode(code))
    lanid='0'
    if lan=='G++':
        lanid = '0'
    elif lan=='gcc':
        lanid = '1';
    elif lan=='java':
        lanid = '2'
    elif lan=='pascal':
        lanid = '3'
    elif lan=='C++':
        lanid = '4'
    elif lan=='C':
        lanid = '5'
    elif lan=='Fortran':
        lanidid = '6'
    postdata2 = urllib.urlencode({
        "problem_id": pro_ojid,
        "language": lanid, #0:G++ 1:gcc;2:java;3:pascal;4:C++;5:C;6:Fortran
        "source": code,
        "submit":"Submit",
        "encoded":"1"
    }).encode('utf-8')
    req3 = urllib2.Request(url3+pro_ojid, postdata2)
    req3.add_header('User-Agent', useragent)
    data3 = urllib2.urlopen(req3).read()
    fhandle3 = open("F:\\biyesheji\\gradu_pro\\base_version\spider_content\\3submit_result.html",'wb')
    fhandle3.write(data3)
    fhandle3.close()
    #返回提交的结果
    time.sleep(5)
    url4 = "http://poj.org/status?problem_id="+pro_ojid+"&user_id=STUDENTOJ&result=&language="
    req4 = urllib2.Request(url4)
    req4.add_header('User-Agent', useragent)
    data4 = urllib2.urlopen(req4).read()
    fhandle4 = open("F:\\biyesheji\\gradu_pro\\base_version\spider_content\\4compile_result.html", "wb")
    fhandle4.write(data4)
    fhandle4.close()
    # 评测结果re
    print '开始爬取评测结果。。。'
    # pat1 ='<a href=showcompileinfo.+?</font>'
    pat1 = '<a href=userstatus.user_id=STUDENTOJ>STUDENTOJ.+?</font>'
    with open('F:\\biyesheji\\gradu_pro\\base_version\\spider_content\\4compile_result.html', 'r') as f:
        html_data = f.read()
    # print html_data
    result = re.search(pat1, html_data)
    # print result.group()
    pat1_content = result.group()
    pat2 = '<font color.+?</font>'
    result = re.search(pat2, pat1_content)
    # print result.group()
    pat2_content = result.group()
    pat3 = '>.+?<'
    result = re.search(pat3, pat2_content)
    # print result.group()
    compile_result = result.group()[1:-1]
    print compile_result
    return render_template('/spider/compile_result.html', msg=compile_result)

