import os
from flask import Flask
from flask import request
from flask import render_template
from flask import json
from flask import session
from flask import redirect
from functools import wraps
#from .secrets import get_secret_image_gallery
from  .db import connect
from .s3_users import put_object, get_object, download_object, delete_object
import json
import psycopg2
from .users.user import User
from .users.postgres_user_dao import PostgresUserDAO
from .secrets import get_secret_flask_session

app = Flask(__name__)
app.secret_key = get_secret_flask_session()
bucket_name = "edu.au.cc.image--gallery"


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'uploads')
DOWNLOAD_FOLDER = os.path.join(APP_ROOT, 'static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER



def get_user_dao():
    return PostgresUserDAO()

connect()

def check_admin():
    return 'username' in session and session['username'] == 'Michael'

def requires_admin(view):
    @wraps(view)
    def decorated(**kwargs):
        if not check_admin():
            return redirect('/login')
        return view(**kwargs)
    return decorated

def requires_user(view):
    @wraps(view)
    def decorated(**kwargs):
        if session['username'] == None:
            return redirect('/login')
        return view(**kwargs)
    return decorated

@app.route('/debugSession')
def debugSession():
    result = ""
    for key,value in session.items():
        result += key+"->"+str(value)+"<br />"
    return result

@app.route('/')
def front_page():
    return render_template('front.html')

@app.route('/invalidLogin')
def invalidLogin():
    return "invalid"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = get_user_dao().select_user(request.form["username"])
        if user is None or user.password != request.form["password"]:
            return redirect('/invalidLogin')
        else:
            session['username'] = request.form["username"]
            return redirect("/")
    else:
        return render_template('login.html')

@app.route('/upload')
@requires_user
def upload():
    return render_template('upload.html')

@app.route('/uploading', methods=['POST'])
@requires_user
def uploading():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        put_object(bucket_name,f.filename,os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        get_user_dao().add_image(f.filename, session['username'])
        return redirect("/upload")

@app.route('/view')
@requires_user
def view():
    names = get_user_dao().get_image_names(session['username'])
    session['name'] = names
    for f in names:
        download_object(bucket_name, f,os.path.join(app.config['DOWNLOAD_FOLDER'], f) )
    return render_template('viewImages.html',images=get_user_dao().get_image_names(session['username']))


@app.route('/deleteImage/<image>')
@requires_user
def delete_image(image):
    delete_object(bucket_name,image)
    get_user_dao().delete_image(image)
    return redirect('/')

@app.route('/admin/users')
@requires_admin
def admin():
    #db.connect()
    #res = db.execute('select * from users')
    #data = res.fetchall()
    #print(data)
    return render_template('admin.html',rows=get_user_dao().get_users())

@app.route('/admin/users/delete/<user>')
@requires_admin
def delete(user):
    #user = request.form['username']
    #res = db.execute("delete from users where username=%s;",(user,))
    get_user_dao().delete_user(user)
    return render_template('complete.html')

@app.route('/admin/users/edit/<username>')
@requires_admin
def edit(username):
    #db.connect()
    #username = request.form['row']
    #row = db.execute("select * from users where username=%s;",(data,))
    #res = row.fetchone()
    return render_template('useredit.html',user=get_user_dao().select_user(username))

@app.route('/admin/users/complete',methods=['POST'])
@requires_admin
def complete():
    #db.connect()
    username = request.form['username']
    password = request.form['password']
    fullname = request.form['fullname']
    #res = db.execute("update users set password=%s, full_name=%s where username=%s;",(password,fullname,username)
    get_user_dao().edit_user(username, password, fullname)
    return render_template('complete.html')

@app.route('/admin/users/add')
@requires_admin
def addpage():
    return render_template('adduser.html')

@app.route('/admin/users/completenew',methods=['POST'])
@requires_admin
def completenew():
    #db.connect()
    username = request.form['username']
    password = request.form['password']
    fullname = request.form['fullname']
    #res = db.execute("insert into users values (%s,%s,%s);",(username,password,fullname))
    get_user_dao().add_user(username, password, fullname)
    return render_template('complete.html')

if __name__ == '__main__':
    app.run()
