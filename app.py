from flask import Flask, render_template, redirect, url_for, request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils import *
app = Flask(__name__)

@app.route('/send/<info>',methods=['GET','POST'])
def send(info):
    if request.method == 'POST':
        recv = request.form['recv']
        mess = request.form['mess']
        subj = request.form['subj']
        url_att = request.form['att']
        user_name = info.split('###')[0]
        pass_word = info.split('###')[1]
        message = prepare_mess(subject=subj,trans=user_name,recv=recv,mess=mess,url_attach=url_att)
        send_email(user_name=user_name,password=pass_word,message=message,receiver=recv)
        return redirect(url_for('mail_box',info=info))
    return render_template('send.html', error=error)
@app.route('/download_pop3/<info>',methods=['GET','POST'])
def download_pop3(info):
    if request.method == 'POST':
        return redirect(url_for('mail_box',info=info))
    return render_template('download_pop3.html',error=error)
@app.route('/choice_protocol/<info>',methods=['GET','POST'])
def choice_protocol(info):
    if request.method == 'POST':
        if request.form['pop3_imap'] == "POP3":
            user_name = info.split('###')[0]
            pass_word = info.split('###')[1]
            check_mail_pop3(user_name=user_name,password=pass_word)
            return redirect(url_for('download_pop3',info=info))
        elif request.form['pop3_imap'] == "IMAP":
            return redirect(url_for('browser_imap',info=info))
        elif request.form['pop3_imap'] == "Quay lại trang chủ":
            return redirect(url_for('mail_box',info=info))
    return render_template('pop3_imap.html',error=error)

@app.route('/mailbox/<info>',methods=['GET','POST'])
def mail_box(info):
    if request.method == 'POST':
        if request.form['submit_button'] == "Soạn thư mới":
            return redirect(url_for('send',info=info))
        elif request.form['submit_button'] == "Hộp thư đến":
            return redirect(url_for('choice_protocol',info=info))
    return render_template('mail_box.html',error=error)

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
            return redirect(url_for('mail_box',info=info))
        #     return render_template('send.html', error=error)
        else:
            # error = 'Invalid Credentials. Please try again.'
            return render_template('index.html', error=error)
    return render_template('index.html', error=error)
counter = -1
@app.route('/imap/<info>',methods=['GET','POST'])
def browser_imap(info):
    global counter
    if request.method == 'POST':
        if request.form['submit_button'] == "Trước đó":
            # if counter > 0:
            counter -= 1
            # else:
            #     counter = 0
        elif request.form['submit_button'] == "Xem tiếp":
            counter += 1
            print(counter)
    user_name = info.split('###')[0]
    pass_word = info.split('###')[1]
    emcont = check_mail_imap(user_name,pass_word,counter)
    header = parse_email_header(emcont)
    body = parse_email_content(emcont)
    return render_template('browser_imap.html', header=header,body=body)
app.run(host='0.0.0.0',port=12345,debug=True)
