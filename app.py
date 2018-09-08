from flask import Flask 
import hashlib
from flask import render_template, request, Response, redirect, current_app
from flask import json
import jdatetime, datetime
import create_month_info
import read_daily_info_from_db

app = Flask(__name__)

ADMIN_USER = 'admin'
ADMIN_PASS_HASH = '67b70652178547867b6488f7548ff1ca'
# password = Sa$Hna7aacK90


def checkAccount(username, password):
    if username == ADMIN_USER and password == ADMIN_PASS_HASH:
        return True
    else:
        return False



@app.route('/home')
def return_charts_data():

    password = request.cookies.get('password_cookie')

    if password == ADMIN_PASS_HASH:
        
        data1 = read_daily_info_from_db.get_daily_info()
        dates1 = data1[0]
        RX1 = data1[1]
        TX1 = data1[2]


        data2 = create_month_info.month_info()
        dates2 = data2[0]
        RX2 = data2[1]
        TX2 = data2[2]

        return render_template('index.html', 
            dates=json.dumps(dates1) , RX=json.dumps(RX1) , TX=json.dumps(TX1),
            dates2=json.dumps(dates2) , RX2=json.dumps(RX2) , TX2=json.dumps(TX2))

    else:
        
        redirect_to_login = redirect('/')
        response = current_app.make_response(redirect_to_login)
        return response 



@app.route('/', methods=['GET', 'POST'])
def login():

    # login proccess
    if request.method == 'POST':

        username = request.form['username'];
        password = request.form['password'];

        password_hash = hashlib.md5(password.encode('utf-8')).hexdigest()

        if checkAccount(username, password_hash):
            # successful login
            redirect_to_login = redirect('/home')
            response = current_app.make_response(redirect_to_login)

            expire_date = datetime.datetime.now()
            expire_date = expire_date + datetime.timedelta(days=7)

            response.set_cookie('username_cookie', value=username, expires=expire_date )
            response.set_cookie('password_cookie', value=password_hash, expires=expire_date )
            return response 

        else:
            # respomse erro to user
            return render_template('login.html', error='invalid-credential')


    # check loged in users
    elif request.method == 'GET':

        password = request.cookies.get('password_cookie')
        
        if password == ADMIN_PASS_HASH:
            redirect_to_login = redirect('/home')
            response = current_app.make_response(redirect_to_login)
            return response 

        else:
            return render_template('login.html')




@app.route('/logout')
def logout():
    redirect_to_login = redirect('/home')
    response = current_app.make_response(redirect_to_login)
    response.delete_cookie("username_cookie")
    response.delete_cookie("password_cookie")
    redirect_to_login = redirect('/')
    return response

