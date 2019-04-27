#-*-coding:utf-8-*-
import os
import sqlite3
from flask import Blueprint,request,session,g,redirect,url_for,abort,render_template,flash
from werkzeug.security import check_password_hash,generate_password_hash
from database_op import get_db
import functools

bp = Blueprint('user',__name__,url_prefix='/user')


@bp.before_app_request #bp.before_app_request() 注册一个 在视图函数之前运行的函数，不论其 URL 是什么。
def load_logged_in_user():
    user_id = session.get('ur_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM oj_user WHERE ur_id = ?',(user_id,)
        ).fetchone()


@bp.route('/register',methods = ['GET','POST'])
def register():
    # load_logged_in_user()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        school = request.form['school']
        grade = request.form['grade']
        isadmin = 0
        db = get_db()
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT ur_id FROM oj_user WHERE name =?',(username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO oj_user (name,password,school,grade,isadmin) VALUES (?,?,?,?,?)',(username,generate_password_hash(password),school,grade,isadmin)
            )
            db.commit()
            return redirect(url_for('user_func.index'))
        flash(error)
    return render_template('user/register.html')


@bp.route('/login',methods = ['POST','GET'])
def login():
    # load_logged_in_user()
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'select * from oj_user where name = ?',(username,)#为什么这里要加一个逗号
        ).fetchone()
        if user == None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'],password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['ur_id'] = user['ur_id']
            session['isadmin'] = user['isadmin']
            if session['isadmin'] == 1:
                return redirect(url_for('admin.index'))
            return redirect(url_for('user_func.index'))
        flash(error)
    return render_template('user/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('user_func.index'))

 #使用装饰器来检查在其他视图执行时是否已经登录
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('user.login'))
        return view(**kwargs)
    return wrapped_view
