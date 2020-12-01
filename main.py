from utils import *
if __name__=='__main__':
    user_name = 'remitai1998@gmail.com'
    password = '10111998tai'
    message = 'I love Computer Network'
    receiver = 'remitai1998@gmail.com'
    smtp_host = 'smtp.gmail.com'
    smtp_port = 465
    # send_email(user_name,password,smtp_host,smtp_port,message,receiver)
    imap_host = 'imap.gmail.com'
    imap_port = '993'
    pop3_host = 'pop.gmail.com'
    pop3_port = '995'
    check_mail_pop3(user_name,password,pop3_host,pop3_port)
    # print(check_mail_imap(user_name,password,imap_host,imap_port))
