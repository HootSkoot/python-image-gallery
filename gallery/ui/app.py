from flask import Flask
from flask import request
from flask import render_template
from flask import json
#from .secrets import get_secret_image_gallery
from  .db import connect
import json
import psycopg2
from .users.user import User
from .users.postgres_user_dao import PostgresUserDAO
app = Flask(__name__)

def get_user_dao():
    return PostgresUserDAO()

connect()

@app.route('/')
def hello_world():
    return 'Hello, Michael!'

@app.route('/goodbye')
def goodbye():
    return 'Goodbye!'

@app.route('/greet/<name>')
def greet(name):
    return 'Nice to meet you ' + name

@app.route('/add/<int:x>/<int:y>', methods = ['GET'])
def add(x,y):
    return 'The sum is ' + str(x + y)

@app.route('/mult',methods=['POST'])
def mult():
    x = request.form['x']
    y = request.form['y']
    return 'The product is ' + str(int(x)*int(y))

@app.route('/calculator/<name>')
def calculator(name):
    return render_template('calculator.html',name=name)

@app.route('/admin')
def admin():
    #db.connect()
    #res = db.execute('select * from users')
    #data = res.fetchall()
    #print(data)
    return render_template('admin.html',rows=get_user_dao().get_users())

@app.route('/delete/<user>')
def delete(user):
    #user = request.form['username']
    #res = db.execute("delete from users where username=%s;",(user,))
    get_user_dao().delete_user(user)
    return render_template('complete.html')

@app.route('/edit/<username>')
def edit(username):
    #db.connect()
    #username = request.form['row']
    #row = db.execute("select * from users where username=%s;",(data,))
    #res = row.fetchone()
    return render_template('useredit.html',user=get_user_dao().select_user(username))

@app.route('/complete',methods=['POST'])
def complete():
    #db.connect()
    username = request.form['username']
    password = request.form['password']
    fullname = request.form['fullname']
    #res = db.execute("update users set password=%s, full_name=%s where username=%s;",(password,fullname,username)
    get_user_dao().edit_user(username, password, fullname)
    return render_template('complete.html')

@app.route('/add')
def addpage():
    return render_template('adduser.html')

@app.route('/completenew',methods=['POST'])
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
