# -*- encoding:utf-8 -*-
import re
#题目内容re
print '开始解析题目。。。'
with open('F:\\biyesheji\gradu_pro\\base_version\spider_content\\2problem_content.html','r') as f:
    pro_content = f.read()
pata = '<div class="ptt" lang="(zh-CN|en-US)">.+?</div>'
presult1 = re.search(pata, pro_content, re.S)
ptitle1 = pro_content[presult1.span()[0]:presult1.span()[1]]
pataa = '>.+?<'
presult2 = re.search(pataa, ptitle1)
ptitle2 = ptitle1[presult2.span()[0]:presult2.span()[1]]
title = ptitle2[1:-1]
print title
# title解决

#评测结果re
print '开始爬取评测结果。。。'
# pat1 ='<a href=showcompileinfo.+?</font>'
pat1 = '<a href=userstatus.user_id=STUDENTOJ>STUDENTOJ.+?</font>'
with open('F:\\biyesheji\\gradu_pro\\base_version\\spider_content\\4compile_result.html','r') as f:
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

