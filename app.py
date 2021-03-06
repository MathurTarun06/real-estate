
from flask import Flask,session,render_template,request,redirect,g,url_for
import mysql.connector
import os

app = Flask(__name__)

app.secret_key = os.urandom(24)


# creating a connection object to connect with mysql database
connection_obj=mysql.connector.connect(host="remotemysql.com",user="8nRN1vkabC",password="C23NPCF8G2",database="8nRN1vkabC")

# var to communicate with database
cursor_obj = connection_obj.cursor()

@app.route("/")
def helloworld():
    return render_template("index.html")


# decorator for user's index after login
@app.route('/index')
def index():
    # if user has key then login to index page
    if 'id' in session:
        return render_template('index.html')
    else:
        return redirect('/')

@app.route('/login_validation', methods=['post'])
def login_validation():
    email= request.form.get('email')
    password = request.form.get('password')

    #query  to check if email exists
    cursor_obj.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'"""
    .format(email,password))
    #store the result from above query in users
    users = cursor_obj.fetchall()

    #if user is found , redirect user to user's indexpage
    if len(users)>0:
        session['id']=users[0][0]

    # redirect to user's index
        return redirect('/index')
    else:
        # redirect to main page to signup
        return redirect('/')

#decorator to register a new user    
@app.route('/add_user', methods=['post'])
def add_user():
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')

    # store the registered user data into db
    cursor_obj.execute("""INSERT INTO `users` (`id`,`name`, `email`, `password`) VALUES 
    (NULL,'{}','{}','{}')""".format(name,email,password))
    connection_obj.commit()

    cursor_obj.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
    myuser = cursor_obj.fetchall()
    session['id'] = myuser[0][0]
    return redirect('/index')

if __name__=="__main__": 
    app.run(debug=True, port=8000)
