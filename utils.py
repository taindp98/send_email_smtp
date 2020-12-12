import base64
from socket import *
import ssl
import poplib
import imaplib
import email
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import math
def check_server_reply(clientSocket):
    recv220 = clientSocket.recv(1024).decode()
    # print('Server :',recv220)
    if recv220[:3] != '220':
        print("220 reply not received from server.")
    heloContent = 'HELO ComputerNetwork'
    heloCommand = '{}\r\n'.format(heloContent).encode()
    # print('Client :',heloContent)
    clientSocket.send(heloCommand)
    recv250 = clientSocket.recv(1024).decode()
    # print('Server :',recv250)
    if recv250[:3] != '250':
        print('250 reply not received from server.')
    authContent = 'AUTH Login'
    authCommand = '{}\r\n'.format(authContent).encode()
    clientSocket.send(authCommand)
    # print('Client :',authContent)
    recv334 = clientSocket.recv(1024).decode()
    # print('Server :',recv334)
def login_mail(user_name,pass_word,host='smtp.gmail.com',port=465):
    """
    login use method send socket
    command login
    """
    clientSocket = socket(AF_INET,SOCK_STREAM)
    clientSocket.connect((host, port))
    context = ssl.create_default_context()
    clientSocket = context.wrap_socket(clientSocket, server_hostname=host)
    check_server_reply(clientSocket)
    clientSocket.send(base64.b64encode(user_name.encode()))
    clientSocket.send ("\r\n".encode ())
    clientSocket.recv(1024).decode()
    clientSocket.send(base64.b64encode(pass_word.encode()))
    clientSocket.send ("\r\n".encode ())
    clientSocket.recv(1024).decode()
    transmitter = user_name
    fromContent = f'MAIL FROM: <{transmitter}>'
    mailCommand = "{}\r\n".format(fromContent).encode()
    clientSocket.send(mailCommand)
    # print('Client :',fromContent)

    recv1 = clientSocket.recv(1024).decode()
    print('Server :',recv1)
    if recv1[:3] != '250':
        print('250 reply not received from server.')
        return False
    else:
        print('Server : Authentication success')
        return True
def authorization_login(user_name,pass_word,clientSocket,message,receiver):
    check_server_reply(clientSocket)
    clientSocket.send(base64.b64encode(user_name.encode()))
    clientSocket.send ("\r\n".encode ())
    clientSocket.recv(1024).decode()
    clientSocket.send(base64.b64encode(pass_word.encode()))
    clientSocket.send ("\r\n".encode ())
    clientSocket.recv(1024).decode()
    transmitter = user_name
    fromContent = f'MAIL FROM: <{transmitter}>'
    mailCommand = "{}\r\n".format(fromContent).encode()
    clientSocket.send(mailCommand)
    # print('Client :',fromContent)
    recv1 = clientSocket.recv(1024).decode()
    # print('Server :',recv1)
    if recv1[:3] != '250':
        print('250 reply not received from server.')
        return False
    rcpContent = f'RCPT TO: <{receiver}>'
    mailCommand = "{}\r\n".format(rcpContent).encode()
    clientSocket.send(mailCommand)
    # print('Client :',rcpContent)
    recv1 = clientSocket.recv(1024).decode()
    # print('Server :',recv1)
    if recv1[:3] != '250':
        print('250 reply not received from server.')
        return False
    dataContent = 'DATA'
    dataCommand = '{}\r\n'.format(dataContent).encode()
    clientSocket.send(dataCommand)
    # print('Client :',dataContent)
    recv1 = clientSocket.recv(1024).decode()
    # print('Server :',recv1)
    if recv1[:3] != '354':
        print('data 354 reply not received from server.')
        return False
    mess = f'{message}\r\n.\r\n'
    clientSocket.send(mess.encode())
    # print('Client :', mess)
    recv1 = clientSocket.recv(1024).decode()
    # print('Server :',recv1)
    if recv1[:3] != '250':
        print('end msg 250 reply not received from server.')
        return False
    quitContent = 'QUIT'
    quitCommand = '{}\r\n'.format(quitContent).encode()
    clientSocket.send(quitCommand)
    # print('Client :', quitContent)
    recv1 = clientSocket.recv(1024).decode()
    # print('Server :',recv1)
    if recv1[:3] != '221':
        print('quit 221 reply not received from server.')
        return False
    return True
def send_email(user_name,password,message,receiver):

    host='smtp.gmail.com'

    port=465

    clientSocket = socket(AF_INET,SOCK_STREAM)
    clientSocket.connect((host, port))
    context = ssl.create_default_context()
    clientSocket = context.wrap_socket(clientSocket, server_hostname=host)
    resp = authorization_login(user_name,password,clientSocket,message,receiver)
    return resp
# def check_mail_pop3(user_name,password,host,port):
def count_mail(user_name,password):
    host = 'imap.gmail.com'
    port = 993
    server = imaplib.IMAP4_SSL(host,port)
    print('-----Authorization-----')
    ser_sta,ser_res = server.login(user_name,password)
    print('Server :',ser_sta)
    print('Server :',ser_res[0].decode('utf-8'))
    print('-----Transaction-----')
    print('Client : Inbox')
    ser_sta,ser_res = server.select("Inbox")
    # print('Server :',ser_sta)
    # print('Server :',ser_res[0].decode('utf-8'))
    index = ser_res[0].decode('utf-8')
    return index
def check_mail_pop3(user_name,password,dele):
    path_save = '/home/taindp/PycharmProjects/email/download_pop3'
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S").replace(r'/',r'_').replace(r':',r'_').replace(r' ',r'_')
    name_save = os.path.join(path_save,dt_string)
    # print(dt_string)
    host = 'pop.gmail.com'
    port = '995'
    server = poplib.POP3_SSL(host, port)
    print('Server :',server.getwelcome().decode('utf-8'))
    server.user(user_name)
    print('Client : user',user_name)
    server.pass_(password)
    # print('Server :',server.retr(1)[0].decode('utf-8'))
    # print('Client : list')
    (messageCount, totalMessageSize) = server.stat()
    print('Server : {} messages in Mailbox'.format(messageCount))
    print('Server : {} total messages size bytes'.format(totalMessageSize))
    resp, mails, octets = server.list()
    # print('Server :', len(mails))
    # print(mails)
    # print('Server :',resp.decode('utf-8'))
    index = len(mails)
    if index > 0:
        # file_save = open(name_save,'w')
        for item in range(0,index):
            file_save = open(str(name_save+'_'+str(item)+'.txt'),'w')
            msg = server.retr(item+1)[1]
            msg_text = b'\r\n'.join(msg).decode('utf-8')
            # print(parse_email_header(msg_text))
            file_save.write(msg_text)
            if dele == True:
                server.dele(item+1)
        # raw_email = b"\n".join(server.retr(1)[1])
        # dict_parser = parser_pop(raw_email)
        server.quit()
    # else:
        return index
    else:
        server.quit()
        return 0
def parser_pop(raw_email):
    parsed_email = email.message_from_bytes(raw_email)
    dict_parser = {}
    dict_parser['From'] = parsed_email['From']
    dict_parser['To'] = parsed_email['To']
    dict_parser['Date'] = parsed_email['Date']
    dict_parser['Subject'] = parsed_email['Subject']
    dict_parser['Text'] = []
    dict_parser['Attachment'] = {}
    for part in parsed_email.walk():
        if part.is_multipart():
            continue
        elif part.get_content_maintype() == 'text':
            text = part.get_payload(decode=True).decode(part.get_content_charset())
            dict_parser['Text'].append(text)
            # print('Text:\n', text)
        # elif part.get_content_maintype() == 'application' and part.get_content_disposition() == 'attachment':
        elif part.get_content_maintype() == 'application':
            name = decode_header(part.get_filename())
            body = part.get_payload(decode=True)
            size = len(body)
            save_path = '/home/taindp/PycharmProjects/email/download_attachment'
            dict_parser['Attachment']['Name'] = name
            dict_parser['Attachment']['Size'] = size
            dict_parser['Attachment']['Body'] = body[0:50]
            fp = open(os.path.join(save_path, name), 'wb')
            fp.write(body)
            # fp.close
            # print('Attachment: "{}", size: {} bytes, starts with: "{}"'.format(name, size, body[:50]))
        # else:
        #     print('Unknown part:', part.get_content_type())
    # print('======== email #%i ended =========' % 1)
    return dict_parser

def decode_header(header):
    decoded_bytes, charset = email.header.decode_header(header)[0]
    if charset is None:
        return str(decoded_bytes)
    else:
        return decoded_bytes.decode(charset)
def cal_len_mailbox_imap(user_name,password):
    host = 'imap.gmail.com'
    port = '993'
    server = imaplib.IMAP4_SSL(host,port)
    server.login(user_name,password)
    server.select("Inbox")
    type,data = server.search(None,'ALL')
    mail_ids = data[0]
    id_list = mail_ids.split()
    return len(id_list)

def check_mail_imap(user_name,password,counter,dele):
    host = 'imap.gmail.com'
    port = '993'
    server = imaplib.IMAP4_SSL(host,port)
    server.login(user_name,password)
    server.select("Inbox")
    type,data = server.search(None,'ALL')
    mail_ids = data[0]
    id_list = mail_ids.split()
    if abs(counter) < len(id_list):
    # response,content = server.fetch(id_list[-1], '(RFC822)' )
        response,content = server.fetch(id_list[counter], '(RFC822)' )
        raw_email = content[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)
        if dele == True:
            server.store(id_list[counter], '+FLAGS', '\\Deleted')
        return email_message
    elif len(id_list) == 1:
        if counter < 0 :
            response,content = server.fetch(id_list[0], '(RFC822)' )
            raw_email = content[0][1]
            raw_email_string = raw_email.decode('utf-8')
            email_message = email.message_from_string(raw_email_string)
            if dele == True:
                server.store(id_list[0], '+FLAGS', '\\Deleted')
            return email_message
        else:
            response,content = server.fetch(id_list[-1], '(RFC822)' )
            raw_email = content[0][1]
            raw_email_string = raw_email.decode('utf-8')
            email_message = email.message_from_string(raw_email_string)
            if dele == True:
                server.store(id_list[-1], '+FLAGS', '\\Deleted')
            return email_message

def parse_email_header(msg):
    header_list = ('From', 'To', 'Subject')
    # loop in the header list
    dict_header = {}
    for header in header_list:
        # get each header value.
        header_value = msg.get(header, '')
        dict_header[header.replace(r':',r'')] = header_value
    return dict_header

# Parse email body data.
def parse_email_body(msg):
    if (msg.is_multipart()):
        # get all email message parts.
        parts = msg.get_payload()
        # loop in above parts.
        for n, part in enumerate(parts):
            content_type = part.get_content_type()
            parse_email_content(msg)
    else:
       parse_email_content(msg)
# Parse email message part data.

def get_attach_imap(msg,down):
    list_name = []
    try:
    # if msg.is_multipart():
        for item in msg.walk():
            maintype = item.get_content_maintype()
            if maintype == 'application':
                body = item.get_payload(decode=True)
                name = decode_header(item.get_filename())
                list_name.append(name)
                if down == True:
                    save_path = '/home/taindp/PycharmProjects/email/download_imap'
                    fp = open(os.path.join(save_path, name), 'wb')
                    fp.write(body)
        return list_name
    except:
        pass
def parse_email_content(msg):
    # messages = []
    body = ""
    if msg.is_multipart():

        for part in msg.walk():
            type = part.get_content_type()
            disp = str(part.get('Content-Disposition'))
            # look for plain text parts, but skip attachments
            if type == 'text/plain' and 'attachment' not in disp:
                charset = part.get_content_charset()
                # decode the base64 unicode bytestring into plain text
                body = part.get_payload(decode=True).decode(encoding=charset, errors="ignore")
                # if we've found the plain/text part, stop looping thru the parts
                break
    else:
        # not multipart - i.e. plain text, no attachments
        charset = msg.get_content_charset()
        body = msg.get_payload(decode=True).decode(encoding=charset, errors="ignore")
    if body:
        return body
def create_header(subject,trans,recv):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = trans
    message["To"] = recv
    return message
def prepare_mess(subject,trans,recv,mess,url_attach):
    message = create_header(subject,trans,recv)
    # attach_file_name = '/home/taindp/Jupyter/resume_3dec/resume_parser/report/20201127_taindp_report_task_ner.pdf'
    part1 = MIMEText(mess, "plain")
    message.attach(part1)
    if url_attach:
        url_attach = os.path.abspath(url_attach)
        attach_file = open(url_attach, 'rb') # Open the file as binary mode
        payload = MIMEBase('application', 'octate-stream', Name=url_attach.split(r'/')[-1])
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload) #encode the attachment
        payload.add_header('Content-Decomposition', 'attachment', filename=url_attach.split(r'/')[-1])
        message.attach(payload)
    return message
