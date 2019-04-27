#-*-coding: utf-8 -*-
import os
from flask import Blueprint,request,session,g,redirect,url_for,abort,render_template,flash
from werkzeug.security import check_password_hash,generate_password_hash
from database_op import get_db, connect_db
import functools
from login_and_register import login_required
from werkzeug.utils import secure_filename
import werkzeug

bp3 = Blueprint('admin', __name__, url_prefix='/admin')


@bp3.route('/index',methods = ['GET','POST'])
@login_required
def index():
    # if request.method == 'POST':
    #     search_content = request.form['search_content']
    #     redirect(url_for('user_func.prolist',search_content))
    return render_template('/admin/index.html')


@bp3.route('/showlist',methods = ['GET','POST'])
@login_required
def showlist():
    # table = request.values.get('table')
    if request.method == 'GET':
        print '这是个GET'
        table = request.values.get('table')
        print table
        db = get_db()
        command = 'SELECT * FROM '+table
        show_entries = db.execute(command).fetchall()
        db.commit()
        db.close()
        # print show_entries
        if table == 'oj_problem':
            print 'oj_problem'
            return render_template('/admin/show_pro.html', show_entries=show_entries)
        elif table == 'oj_user':
            print 'oj_user'
            return render_template('/admin/show_user.html',show_entries=show_entries)
    elif request.method == 'POST':
        table = request.form['table']
        searchcontent = request.form['search_content']
        db = get_db()
        if table=='oj_problem':
            command = 'SELECT * FROM oj_problem WHERE class like \'%'+searchcontent+'%\' OR title like \'%'+searchcontent+'%\' OR pr_id like \'%'+searchcontent+'%\''
            show_entries = db.execute(command).fetchall()
            db.commit()
            db.close()
            return render_template('/admin/show_pro.html', show_entries=show_entries)
        elif table=='oj_user':
            command = 'SELECT * FROM oj_user WHERE ur_id like \'%'+searchcontent+'%\' OR name like \'%'+searchcontent+'%\' OR school like \'%'+searchcontent+'%\' OR grade like \'%'+searchcontent+'%\''
            show_entries = db.execute(command).fetchall()
            db.commit()
            db.close()
            return render_template('/admin/show_user.html', show_entries=show_entries)


@bp3.route('/delete_user')
@login_required
def delete_user():
    ur_id = request.values.get('ur_id')
    db = get_db()
    command = 'DELETE FROM oj_user WHERE ur_id=' + ur_id
    db.execute(command)
    db.commit()
    db.close()
    return redirect(url_for('admin.showlist', table='oj_user'))

@bp3.route('/create_user',methods=['POST','GET'])
@login_required
def create_user():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        school = request.form['school']
        grade = request.form['grade']
        telephone = request.form['telephone']
        isadmin = request.form['isadmin']
        db = get_db()
        error = None
        if not name:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT ur_id FROM oj_user WHERE name =?',(name,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(name)

        if error is None:
            db.execute(
                'INSERT INTO oj_user (name,password,school,grade,telephone,isadmin) VALUES (?,?,?,?,?,?)',(name,generate_password_hash(password),school,grade,telephone,isadmin)
            )
            db.commit()
            # return redirect(url_for('admin.create_user'))
            return redirect(url_for('admin.showlist', table='oj_user'))
        flash(error)
    elif request.method == 'GET':
        return render_template('/admin/create_user.html')
    return render_template('/admin/create_user.html')

@bp3.route('/delete_pro')
@login_required
def delete_pro():
    pr_id = request.values.get('pr_id')
    db = get_db()
    command = 'DELETE FROM oj_problem WHERE pr_id='+pr_id
    db.execute(command)
    db.commit()
    db.close()
    return redirect(url_for('admin.showlist', table='oj_problem'))

@bp3.route('/create_pro',methods=['GET','POST'])
@login_required
def create_pro():
    f_title=None
    f_img_path=None
    f_txt_path=None
    f_pdf_path=None
    f_class=None
    f_prolevel=None
    f_tag=None
    input_datapath=None
    output_datapath=None
    if request.method == 'POST':
        f_title = request.form['title']
        f_class = request.form['pro_class']
        f_prolevel = request.form['pro_level']
        f_tag = request.form['tag']
        f_txt = request.files['txt']
        f_pdf = request.files['pdf']
        f_img = request.files['img']
        f_inputdata1 = request.files['input_data1']
        f_inputdata2 = request.files['input_data2']
        f_inputdata3 = request.files['input_data3']
        f_inputdata4 = request.files['input_data4']
        f_inputdata5 = request.files['input_data5']

        f_outputdata1 = request.files['output_data1']
        f_outputdata2 = request.files['output_data2']
        f_outputdata3 = request.files['output_data3']
        f_outputdata4 = request.files['output_data4']
        f_outputdata5 = request.files['output_data5']

        # print f_img.filename,type(f_img.filename)
        # print f_pdf.filename,type(f_pdf.filename)
        basepath = 'F:/biyesheji/gradu_pro/base_version/problem'
        db = get_db()
        max_id = db.execute('SELECT MAX(pr_id) FROM oj_problem').fetchall()
        print max_id
        if max_id[0][0] is None:
            db.execute('update sqlite_sequence set seq =\'0\' where name =\'oj_problem\'')
            new_id = str(1)
        else:
            new_id = str(int(max_id[0][0])+1)
        upload_path = os.path.join(basepath, new_id)
        isexist = os.path.exists(upload_path)
        if not isexist:
            os.makedirs(upload_path)
        if f_txt.filename != u'':
            f_txt_path = os.path.join(upload_path, new_id+'.txt')
            f_txt.save(f_txt_path)
        if f_pdf.filename != u'':
            f_pdf_path = os.path.join(upload_path, new_id + '.pdf')
            f_pdf.save(f_pdf_path)
        if f_img.filename != u'':
            f_img_path = os.path.join(upload_path, new_id + '.img')
            f_img.save(f_img_path)

        input_datapath = os.path.join(upload_path, 'input')
        isexist = os.path.exists(input_datapath)
        if not isexist:
            os.makedirs(input_datapath)
        output_datapath = os.path.join(upload_path, 'output')
        isexist = os.path.exists(output_datapath)
        if not isexist:
            os.makedirs(output_datapath)
        if f_inputdata1.filename != u'':
            f_inputdata1_path = os.path.join(input_datapath, new_id+'_input_1.txt')
            f_inputdata1.save(f_inputdata1_path)
        if f_inputdata2.filename != u'':
            f_inputdata2_path = os.path.join(input_datapath, new_id+'_input_2.txt')
            f_inputdata2.save(f_inputdata2_path)
        if f_inputdata3.filename != u'':
            f_inputdata3_path = os.path.join(input_datapath, new_id+'_input_3.txt')
            f_inputdata3.save(f_inputdata3_path)
        if f_inputdata4.filename != u'':
            f_inputdata4_path = os.path.join(input_datapath, new_id+'_input_4.txt')
            f_inputdata4.save(f_inputdata4_path)
        if f_inputdata5.filename != u'':
            f_inputdata5_path = os.path.join(input_datapath, new_id+'_input_5.txt')
            f_inputdata5.save(f_inputdata5_path)

        if f_outputdata1.filename != u'':
            f_outputdata1_path = os.path.join(output_datapath, new_id+'_output_1.txt')
            f_outputdata1.save(f_outputdata1_path)
        if f_outputdata2.filename != u'':
            f_outputdata2_path = os.path.join(output_datapath, new_id+'_output_2.txt')
            f_outputdata2.save(f_outputdata2_path)
        if f_outputdata3.filename != u'':
            f_outputdata3_path = os.path.join(output_datapath, new_id+'_output_3.txt')
            f_outputdata3.save(f_outputdata3_path)
        if f_outputdata4.filename != u'':
            f_outputdata4_path = os.path.join(output_datapath, new_id+'_output_4.txt')
            f_outputdata4.save(f_outputdata4_path)
        if f_outputdata5.filename != u'':
            f_outputdata5_path = os.path.join(output_datapath, new_id+'_output_5.txt')
            f_outputdata5.save(f_outputdata5_path)

        # db = get_db()
        db.execute(
            'INSERT INTO oj_problem(title, img_url, txt_url, pdf_url, class, pro_level, tag, input_url, output_url) VALUES (?,?,?,?,?,?,?,?,?)',
            (f_title, f_img_path, f_txt_path, f_pdf_path, f_class, f_prolevel, f_tag, input_datapath, output_datapath )
        )
        db.commit()
        db.close()
        flash('save successfully')
        return redirect(url_for('admin.showlist', table='oj_problem'))

    elif request.method == 'GET':
        return render_template('/admin/create_pro.html')
    return render_template('/admin/create_pro.html')


# if __name__ == '__main__':
#     basepath = 'F:/biyesheji/gradu_pro/base_version/problem'
#     new_id = str(2)
#     upload_path = os.path.join(basepath, new_id)
#     print upload_path
#     db = connect_db()
#     content = db.execute('SELECT pr_id FROM oj_problem').fetchall()
#     print content
#     print len(content)
#     db.close()







