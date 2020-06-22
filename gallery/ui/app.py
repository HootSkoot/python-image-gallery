from flask import Flask
from flask import request
from flask import render_template
from flask import json
from .secrets import get_secret_image_gallery
import json
import psycopg2

app = Flask(__name__)

db_name = "image_gallery"

connection = None


def get_secret():
    jsonString = get_secret_image_gallery()
    return json.loads(jsonString)

def get_password(secret):
    return secret['password']
def get_host(secret):
    return secret['host']
def get_username(secret):
    return secret['username']
def get_dbname(secret):
    return secret['database_name']

def connect():
    global connection
    secret = get_secret()
    connection = psycopg2.connect(host=get_host(secret), dbname=get_dbname(secret), user=get_username(secret), password=get_password(secret))
    connection.set_session(autocommit=True)

def execute(query,args=None):
    global connection
    cursor = connection.cursor()
    if not args:
        cursor.execute(query)
    else:
        cursor.execute(query, args)
    return cursor



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
    connect()
    res = execute('select * from users')
    #data = res.fetchall()
    #print(data)
    return render_template('admin.html',rows=res)

@app.route('/delete/<string:user>',methods=['GET'])
def delete(user):
    #user = request.form['username']
    res = execute("delete from users where username=%s;",(user,))
    return render_template('complete.html')

@app.route('/useredit',methods=['POST'])
def edit():
    connect()
    data = request.form['row']
    row = execute("select * from users where username=%s;",(data,))
    res = row.fetchone()
    return render_template('useredit.html',username=res[0],password=res[1],fullname=res[2])

@app.route('/complete',methods=['POST'])
def complete():
    connect()
    username = request.form['username']
    password = request.form['password']
    fullname = request.form['fullname']
    res = execute("update users set password=%s, full_name=%s where username=%s;",(password,fullname,username))
    return render_template('complete.html')

@app.route('/add')
def addpage():
    return render_template('adduser.html')

@app.route('/completenew',methods=['POST'])
def completenew():
    connect()
    username = request.form['username']
    password = request.form['password']
    fullname = request.form['fullname']
    res = execute("insert into users values (%s,%s,%s);",(username,password,fullname))
    return render_template('complete.html')

if __name__ == '__main__':
    app.run()
