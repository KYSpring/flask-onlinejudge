# -*- coding:utf-8 -*-
import sqlite3
from werkzeug.security import check_password_hash,generate_password_hash
from flask import g


def connect_db():
    rv = sqlite3.connect('myoj.db')
    rv.row_factory = sqlite3.Row #设置返回的查询结果的形态
    return rv


def get_db():
    if not hasattr(g,'db'):
        g.db = connect_db()
    return g.db


def ini_database():
    rv = sqlite3.connect('myoj.db')
    print "open database successfully"
    with open('initial.sql', 'r') as f:
        print f.read()
        rv.executescript(f.read())
    print "the oj_database has been initialized"
    # rv.execute(
    #     'INSERT INTO oj_user(name,password,school,grade,isadmin) VALUES (?,?,?,?,?)',('admin',generate_password_hash('admin'),'school1','grade1','1')
    # )
    # x = rv.execute('select * from oj_user').fetchall()
    # print x
    rv.commit()
    rv.close()
    return

if __name__ == '__main__':
    ini_database()
    rv = connect_db()
    # rv.execute('INSERT INTO oj_problem(title,txt_url,class,pro_level,input_url,output_url) VALUES (?,?,?,?,?,?)',
    #            (u'A+B',u'F:/biyesheji/gradu_pro/base_version/problem/1/1.txt',u'basic',u'简单',
    #             u'F:/biyesheji/gradu_pro/base_version/problem/1/input',
    #             u'F:/biyesheji/gradu_pro/base_version\problem/1/output')
    #            )
    rv.execute('DELETE FROM oj_user where name = \'admin\';')
    rv.execute('INSERT INTO oj_user(name,password,isadmin) VALUES(?,?,?);',
               ('admin', generate_password_hash('admin'), '1'))
    x = rv.execute('select * from oj_user').fetchall()
    print x
    rv.commit()
    rv.close()
#     ini_database()
