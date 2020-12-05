from utils import *
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
if __name__=='__main__':
    user_name = 'remitai1998@gmail.com'
    password = '10111998tai'
    receiver = 'remitai1998@gmail.com'
    # message = 'I love Computer Network'
    message = MIMEMultipart("alternative")
    message["Subject"] = "Demo Mail Client"
    message["From"] = user_name
    message["To"] = receiver
    text = """\
    I love Computer Network
    """
    html = """
    """
    # part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    # message.attach(part1)
    message.attach(part2)

    # smtp_host = 'smtp.gmail.com'
    # smtp_port = 465s
    send_email(user_name,password,message,receiver)
    imap_host = 'imap.gmail.com'
    imap_port = '993'
    pop3_host = 'pop.gmail.com'
    pop3_port = '995'
    # print(login_mail(user_name,password))
    # check_mail_pop3(user_name,password,pop3_host,pop3_port)
    # print(check_mail_imap(user_name,password,imap_host,imap_port))
