from flask import Flask, render_template, request, Response, redirect, current_app, json
import hashlib, jdatetime, datetime
import jalali_charts_info, gregorian_charts_info, config


app = Flask(__name__)


ADMIN_USER = config.user
ADMIN_PASS_HASH = config.password

#### If you want to have gegorian date form in your charts uncomment gregorian 
# DATE = "gregorian"
DATE = "jalali"
    


def checkAccount(username, password):
    if username == ADMIN_USER and password == ADMIN_PASS_HASH:
        return True
    else:
        return False


@app.route('/home')
def return_charts_data():

    password = request.cookies.get('password_cookie')

    if password == ADMIN_PASS_HASH:
        
        if DATE == "jalali" :
            date_form = jalali_charts_info

        elif DATE == "gregorian":
            date_form =  gregorian_charts_info


        data1  = date_form.get_daily_info()
        dates1 = data1[0]
        RX1    = data1[1]
        TX1    = data1[2]


        data2  = date_form.month_info()
        dates2 = data2[0]
        RX2    = data2[1]
        TX2    = data2[2]


        return render_template('index.html', 
            dates1=json.dumps(dates1) , RX1=json.dumps(RX1) , TX1=json.dumps(TX1),
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
            # response error to user
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

