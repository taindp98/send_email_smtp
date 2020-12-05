from flask import Flask, render_template, redirect, url_for, request
from utils import *
app = Flask(__name__)

@app.route('/send/<info>',methods=['GET','POST'])
def login_success(info):
    if request.method == 'POST':
        recv = request.form['recv']
        mess = request.form['mess']
        user_name = info.split('###')[0]
        pass_word = info.split('###')[1]
        # print(user_name)
        # print(pass_word)
        send_email(user_name=user_name,password=pass_word,message=mess,receiver=recv)
    return render_template('test_send_fl_login.html', error=error)


@app.route('/fail')
def login_failed():
    return "Login Failed"
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user_name = request.form['username']
        pass_word = request.form['password']
        if login_mail(user_name=user_name,pass_word=pass_word):
        # if request.form['username'] != 'remitai1998@gmail.com' or request.form['password'] != '10111998tai':
            info = user_name+'###'+pass_word
            return redirect(url_for('login_success',info=info))
        #     return render_template('send.html', error=error)
        else:
            # error = 'Invalid Credentials. Please try again.'
            return redirect(url_for('login_failed'))
    return render_template('index.html', error=error)

app.run(host='0.0.0.0',port=12345,debug=True)
