from utils import *
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import date,datetime
if __name__=='__main__':
    user_name = 'remitai1998@gmail.com'
    password = '10111998tai'
    receiver = 'remitai1998@gmail.com'
    # message = 'I love Computer Network'
    # message = MIMEMultipart("alternative")
    # message["Subject"] = "Demo Mail Client"
    # message["From"] = user_name
    # message["To"] = receiver
    # text = """\
    # I love Computer Network"""
    # html = """
    # """
    # # message.attach(MIMEText(text, 'plain'))
    # attach_file_name = '/home/taindp/Jupyter/resume_3dec/resume_parser/report/20201127_taindp_report_task_ner.pdf'
    # attach_file = open(attach_file_name, 'rb') # Open the file as binary mode
    # payload = MIMEBase('application', 'octate-stream', Name=attach_file_name.split(r'/')[-1])
    # payload.set_payload((attach_file).read())
    # encoders.encode_base64(payload) #encode the attachment
    # payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name.split(r'/')[-1])
    # #add payload header with filename
    # part1 = MIMEText(text, "plain")
    # message.attach(part1)
    # message.attach(payload)
    # smtp_host = 'smtp.gmail.com'
    # smtp_port = 465s
    subject = 'Demo Dec7'
    trans = 'remitai1998@gmail.com'
    recv = 'remitai1998@gmail.com'
    mess = 'Good morning'
    # open(path,'r')
    # url_attach = '/home/taindp/Jupyter/resume_3dec/resume_parser/report/20201127_taindp_report_task_ner.pdf'
    # message = prepare_mess(subject,trans,recv,mess,url_attach)
    # send_email(user_name,password,message,receiver)
    # imap_host = 'imap.gmail.com'
    # imap_port = '993'
    # pop3_host = 'pop.gmail.com'
    # pop3_port = '995'
    # print(login_mail(user_name,password))
    print(check_mail_pop3(user_name,password))
    # emcont = (check_mail_imap(user_name,password,-1,False))
    # print(parse_email_header(emcont))
    # print(emcont)
    # for item in emcont.walk():
    #     print(item.get_content_maintype())
    # print(emcont)
    # print(get_attach_imap(emcont))
    # parse_email_content(emcont)
    # print((int((b'1').decode())))
    # today = date.today()
    # now = datetime.now()
    # dt_string = now.strftime("%d/%m/%Y %H:%M:%S").replace(r'/',r'_').replace(r':',r'_').replace(r' ',r'_')
    # print(dt_string)
