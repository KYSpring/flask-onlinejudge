#-*-coding:utf-8-*-
import datetime,signal
import os
import subprocess
from run_cmd import getstatusoutput
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from login_and_register import login_required
from flask import Blueprint,request,session,g,redirect,url_for,abort,render_template,flash
from werkzeug.security import check_password_hash,generate_password_hash
from database_op import get_db
import functools
import threading
import time
path = 'F:\\biyesheji\\gradu_pro\\base_version\\problem'
bp2 = Blueprint('user_func',__name__,url_prefix='/user_func')
time_out = 10


def run_python3(id=1):
    input_dir = path + '/' + str(id) + '/input'
    output_dir = path + '/' + str(id) + '/output'
    file_path = path + '/newpython3.py'
    total_case = -1
    count = 0
    for root, dirs, files in os.walk(input_dir):
        total_case = len(files)
        for file in files:
            input_f = open(input_dir + '/' + file, 'r')
            input_data = input_f.read()
            input_f.close()
            # print list(input_data)
            output_f = open(output_dir+'/'+file.replace('input','output'))
            ans = output_f.read()
            output_f.close()
            #测试
            # F:\anaconda\content\python.exe
            # obj1 = subprocess.Popen('F:\\anaconda\content\python.exe --version', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # cmd_out1 = obj1.stdout.read()
            # obj1.stdout.close()
            # cmd_error1 = obj1.stderr.read()
            # obj1.stderr.close()
            # print cmd_out1,cmd_error1
            command = 'F:\\anaconda\\content\\python.exe ' + file_path  #此处若直接输入python，会默认为Python2版本，还没搞清楚为什么
            print 'this is :'+command
            start = datetime.datetime.now()
            obj = subprocess.Popen(command, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            obj.stdin.write(input_data)
            obj.stdin.close()
            while obj.poll() is None:
                time.sleep(1)
                now = datetime.datetime.now()
                if (now - start).seconds > time_out:
                    os.popen('taskkill.exe /f /pid:' + str(obj.pid), 'r')
                    print obj.pid
                    sta = 0
                    msg = "运行超时"
                    return sta, msg
            cmd_out = obj.stdout.read()
            obj.stdout.close()
            cmd_error = obj.stderr.read()
            userans = list(cmd_out)
            if len(userans) != 0 :
                userans.pop()
                userans.pop()
            obj.stderr.close()
            # print cmd_out  # 测试输出
            # print cmd_error  # 同上
            print list(ans)
            print list(cmd_out)
            if cmd_error != '':
                msg = cmd_error
                return 0, msg
            elif list(ans) == userans:
                count = count + 1
    msg = '通过样例数：' + str(count) + '；总样例数：' + str(total_case) + '；通过率：' + str(count / total_case * 100) + '%'
    return 1, msg


def run_python2(id=2):
    input_dir = path + '/' + str(id) + '/input'
    output_dir = path + '/' + str(id) + '/output'
    file_path = path + '/newpython2.py'
    total_case = -1
    count = 0
    for root, dirs, files in os.walk(input_dir):
        total_case = len(files)
        for file in files:
            input_f = open(input_dir+'/'+file, 'r')
            input_data = input_f.read()
            input_f.close()
            # print list(input_data)
            output_f = open(output_dir+'/'+file.replace('input','output'))
            ans = output_f.read()
            # print list(ans)
            output_f.close()
            command = 'python2 '+file_path
            # print command
            start = datetime.datetime.now()
            obj = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            obj.stdin.write(input_data)
            obj.stdin.close()
            while obj.poll() is None:
                time.sleep(1)
                now = datetime.datetime.now()
                if (now - start).seconds > time_out:
                    os.popen('taskkill.exe /f /pid:' + str(obj.pid), 'r')
                    print obj.pid
                    sta = 0
                    msg = "运行超时"
                    return sta, msg
            cmd_out = obj.stdout.read()
            obj.stdout.close()
            cmd_error = obj.stderr.read()
            obj.stderr.close()
            # print list(cmd_out) #测试输出
            # print cmd_error #同上
            if cmd_error != '':
                msg = cmd_error
                return 0, msg
            elif list(cmd_out) == list(ans):
                count = count+1
    msg = '通过样例数：'+str(count)+'；总样例数：'+str(total_case)+'；通过率：'+str(float(count)/total_case*100)+'%'
    global time_pass
    time_pass = 1
    return 1, msg


def run_cpp(id = 1):
    input_dir = path+'/'+str(id)+'/input'
    output_dir = path+'/'+str(id)+'/output'
    # command1 = 'cd ' + path
    # command2 = 'f:'
    # command3 = 'g++ -o newcpp newcpp.cpp'
    # command4 = 'newcpp.exe <1_input.txt> output_tmp.txt'
    # command = command1 + '&&' + command2 + '&&' + command3
    command = "g++ -o F:\\biyesheji\\gradu_pro\\base_version\\problem\\newcpp F:\\biyesheji\gradu_pro\\base_version\\problem\\newcpp.cpp"
    print command
    # s, r = getstatusoutput(command)
    pipe = os.popen(command, 'r')
    s = pipe.close()
    if s is None:
        s = 0
    count = 0  # 用于测试样例计数
    total_case = 0
    if s == 1:
        msg = '编译出错，请检查代码是否有逻辑或语法错误'
        sta = 0
        return sta, msg
    else:
        for root,dirs,files in os.walk(input_dir):
            total_case = len(files)
            for input_file in files:
                input_file_path = input_dir+'/'+input_file
                # command4 = 'F:\\biyesheji\\gradu_pro\\base_version\\problem\\newcpp.exe <'+input_file_path+'> F:\\biyesheji\\gradu_pro\\base_version\\problem\\output_tmp.txt'
                command4 = 'F:\\biyesheji\\gradu_pro\\base_version\\problem\\newcpp.exe'
                input_f = open(input_file_path, 'r')
                input_data = input_f.read()
                start = datetime.datetime.now()
                process = subprocess.Popen(command4, stdin=subprocess.PIPE,
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                process.stdin.write(input_data)
                process.stdin.close()
                while process.poll() is None:
                    time.sleep(1)
                    now = datetime.datetime.now()
                    if(now - start).seconds > time_out:
                        os.popen('taskkill.exe /f /pid:' + str(process.pid), 'r')
                        print process.pid
                        sta = 0
                        msg = "运行超时"
                        return sta, msg
                # pipe = os.popen(command, 'r')
                # pipe.close()
                cmd_out = process.stdout.read()
                process.stdout.close()
                with open(path + '/output_tmp.txt', 'w')as f_out:
                    f_out.write(cmd_out)
                output_tmp_f = open(path+'/output_tmp.txt', 'r')
                userans = output_tmp_f.read()
                output_tmp_f.close()
                ans_filename = input_file.replace('input','output')
                ans_f = open(output_dir+'/'+ans_filename)
                ans = ans_f.read()
                ans_f.close()
                print list(ans)
                print list(userans)
                if ans == userans:
                    count = count+1
        msg = '通过样例数：'+str(count)+'；总样例数：'+str(total_case)+'；通过率：'+str(float(count)/total_case*100)+'%'
        sta = 1
        return sta, msg


@bp2.route('/index',methods = ['GET','POST'])
def index():
    # if request.method == 'POST':
    #     search_content = request.form['search_content']
    #     redirect(url_for('user_func.prolist',search_content))
    return render_template('/user/index.html')


@bp2.route('/pro_list',methods = ['GET','POST'])
@login_required
def pro_list(pro_class=None):
    pro_class = request.values.get("pro_class")
    if request.method == 'POST':
        print '这是个POST'
        searchcontent = request.form['search_content']
        db = get_db()
        command = 'SELECT * FROM oj_problem WHERE class like \'%'+searchcontent+\
                  '%\' OR title like \'%'+searchcontent+'%\' OR pr_id like \'%'+searchcontent+'%\''
        print command
        pro_entries = db.execute(
            # 'SELECT pr_id,title,img_url,txt_url,pdf_url,class,pro_level,tag,input_url,output_url'
            command
        ).fetchall()
        db.close()
        return render_template('/user/pro_list.html', pro_entries=pro_entries)
    elif request.method == 'GET':
        # print '这是个GET'
        if pro_class is not None:
            db = get_db()
            command = 'SELECT * FROM oj_problem WHERE class like \'%'+pro_class+'%\''
            # print command
            pro_entries = db.execute(
                command
              # 'SELECT pr_id,title,img_url,txt_url,pdf_url,class,pro_level,tag,input_url,output_url'
            ).fetchall()
            return render_template('/user/pro_list.html',pro_entries=pro_entries)
    print '这是else'
    db = get_db()
    pro_entries = db.execute(
       # 'SELECT pr_id,title,img_url,txt_url,pdf_url,class,pro_level,tag,input_url,output_url'
        'SELECT *'
        'FROM oj_problem'
    ).fetchall()
    db.close()
    return render_template('/user/pro_list.html', pro_entries=pro_entries)


@bp2.route('/online_judge',methods = ['GET', 'POST'])
# @login_required
def online_judge():
    pr_id = request.values.get('pr_id')
    if request.method == 'POST':
        code_content = request.form['code']
        if request.form['language'] == 'c/c++':
            with open(path+'/newcpp.cpp', 'w+') as f:
                f.write(code_content)
            flash('submit successfully!')
            sta, msg = run_cpp(pr_id)
            return render_template('/user/compile_result.html', msg=msg, sta=sta)
        elif request.form['language'] == 'python2':
            with open(path+'/newpython2.py', 'w+')as f:
                f.write(code_content)
            flash('submit successfully!')
            sta, msg = run_python2(pr_id)
            return render_template('/user/compile_result.html',msg=msg, sta=sta)
        elif request.form['language']=='python3':
            with open(path+'/newpython3.py','w+')as f:
                f.write(code_content)
            flash('submit successfully!')
            sta, msg = run_python3(pr_id)
            return render_template('/user/compile_result.html', msg=msg, sta=sta)
    db = get_db()
    command = 'select pr_id,title,img_url,txt_url,pdf_url,class,pro_level,tag,input_url,output_url from oj_problem where pr_id = '+ pr_id
    rec = db.execute(command).fetchone()
    g.pr_id = rec['pr_id']
    g.title = rec['title']
    print g.title
    g.img_url = rec['img_url']
    print g.img_url
    g.pro_class = rec['class']
    g.pro_level = rec['pro_level']
    g.tag = rec['tag']
    g.input_url = rec['input_url']
    print g.input_url
    g.output_url = rec['output_url']
    print g.output_url
    if rec['txt_url'] is not None:
        with open(rec['txt_url'], 'r') as f_txt:
            g.describe = f_txt.read().decode('gbk').encode('utf-8')
        print rec['txt_url']
    elif rec['pdf_url'] is not None:
        with open(rec['pdf_url'], 'r') as f_pdf:
            g.describe = f_pdf.read()
        print rec['pdf_url']
    return render_template('user/submit.html')
    g.pop('title')
    g.pop('img_url')
    g.pop('txt_url')
    g.pop('pdf_url')
    g.pop('input_url')
    g.pop('output_url')


@bp2.route('/spider')
def spider():
    return render_template('/spider/search.html')


