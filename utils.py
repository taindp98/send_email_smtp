import base64
from socket import *
import ssl
import poplib
import imaplib
import email
import os
def check_server_reply(clientSocket):
    recv220 = clientSocket.recv(1024).decode()
    print('Server :',recv220)
    if recv220[:3] != '220':
        print("220 reply not received from server.")
    heloContent = 'HELO ComputerNetwork'
    heloCommand = '{}\r\n'.format(heloContent).encode()
    print('Client :',heloContent)
    clientSocket.send(heloCommand)
    recv250 = clientSocket.recv(1024).decode()
    print('Server :',recv250)
    if recv250[:3] != '250':
        print('250 reply not received from server.')
    authContent = 'AUTH Login'
    authCommand = '{}\r\n'.format(authContent).encode()
    clientSocket.send(authCommand)
    print('Client :',authContent)
    recv334 = clientSocket.recv(1024).decode()
    print('Server :',recv334)
def login_mail(user_name,pass_word,host='smtp.gmail.com',port=465):
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
    # print('Server :',recv1)
    if recv1[:3] != '250':
        # print('250 reply not received from server.')
        return False
    else:
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
    print('Client :',fromContent)
    recv1 = clientSocket.recv(1024).decode()
    print('Server :',recv1)
    if recv1[:3] != '250':
        print('250 reply not received from server.')
        return False
    rcpContent = f'RCPT TO: <{receiver}>'
    mailCommand = "{}\r\n".format(rcpContent).encode()
    clientSocket.send(mailCommand)
    print('Client :',rcpContent)
    recv1 = clientSocket.recv(1024).decode()
    print('Server :',recv1)
    if recv1[:3] != '250':
        print('250 reply not received from server.')
        return False
    dataContent = 'DATA'
    dataCommand = '{}\r\n'.format(dataContent).encode()
    clientSocket.send(dataCommand)
    print('Client :',dataContent)
    recv1 = clientSocket.recv(1024).decode()
    print('Server :',recv1)
    if recv1[:3] != '354':
        print('data 354 reply not received from server.')
        return False
    mess = f'{message}\r\n.\r\n'
    clientSocket.send(mess.encode())
    print('Client :', mess)
    recv1 = clientSocket.recv(1024).decode()
    print('Server :',recv1)
    if recv1[:3] != '250':
        print('end msg 250 reply not received from server.')
        return False
    quitContent = 'QUIT'
    quitCommand = '{}\r\n'.format(quitContent).encode()
    clientSocket.send(quitCommand)
    print('Client :', quitContent)
    recv1 = clientSocket.recv(1024).decode()
    print('Server :',recv1)
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
def check_mail_pop3(user_name,password,host,port):
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
        print('Client : retr',index)
        msg = server.retr(index)
        response = msg[0]
        # print('Server :',response.decode('utf-8'))
        lines = msg[1]
        octets = msg[2]
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        print('Server :',msg_content)
        print('Client : quit')
        # print('Server : +OK POP3 server signing off')
        # server.rset()
        # for item in range(1,len(mails)):
        #     server.dele(item)
        server.quit()
        return msg_content
    else:
        return ('Server : Mailbox empty')

def check_mail_imap(user_name,password,host,port):
    server = imaplib.IMAP4_SSL(host,port)
    server.login(user_name,password)
    server.select("Inbox")
    type,data = server.search(None,'ALL')
    mail_ids = data[0]
    id_list = mail_ids.split()
    response,content = server.fetch(id_list[-1], '(RFC822)' )
    raw_email = content[0][1]
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)
    return email_message


def parse_email_header(msg):
    print('********************************* start parse_email_header *********************************')
    # just parse from, to, subject header value.
    header_list = ('From', 'To', 'Subject')

    # loop in the header list
    for header in header_list:
        # get each header value.
        header_value = msg.get(header, '')
        print(header + ' : ' + header_value)

# Parse email body data.
def parse_email_body(msg):
    print('********************************* start parse_email_body *********************************')

    # if the email contains multiple part.
    if (msg.is_multipart()):
        # get all email message parts.
        parts = msg.get_payload()
        # loop in above parts.
        for n, part in enumerate(parts):
            # get part content type.
            content_type = part.get_content_type()
            print('---------------------------Part ' + str(n) + ' content type : ' + content_type + '---------------------------------------')
            parse_email_content(msg)
    else:
       parse_email_content(msg)
# Parse email message part data.
def parse_email_content(msg):
    # get message content type.
    content_type = msg.get_content_type().lower()

    print('---------------------------------' + content_type + '------------------------------------------')
    # if the message part is text part.
    if content_type=='text/plain' or content_type=='text/html':
        # get text content.
        content = msg.get_payload(decode=True)
        # get text charset.
        charset = msg.get_charset()
        # if can not get charset.
        if charset is None:
            # get message 'Content-Type' header value.
            content_type = msg.get('Content-Type', '').lower()
            # parse the charset value from 'Content-Type' header value.
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
                pos = charset.find(';')
                if pos>=0:
                    charset = charset[0:pos]
        if charset:
            content = content.decode(charset)

        print(content)
    # if this message part is still multipart such as 'multipart/mixed','multipart/alternative','multipart/related'
    elif content_type.startswith('multipart'):
        # get multiple part list.
        body_msg_list = msg.get_payload()
        # loop in the multiple part list.
        for body_msg in body_msg_list:
            # parse each message part.
            parse_email_content(body_msg)
    # if this message part is an attachment part that means it is a attached file.
    elif content_type.startswith('image') or content_type.startswith('application'):
        # get message header 'Content-Disposition''s value and parse out attached file name.
        attach_file_info_string = msg.get('Content-Disposition')
        prefix = 'filename="'
        pos = attach_file_info_string.find(prefix)
        attach_file_name = attach_file_info_string[pos + len(prefix): len(attach_file_info_string) - 1]

        # get attached file content.
        attach_file_data = msg.get_payload(decode=True)
        # get current script execution directory path.
        current_path = os.path.dirname(os.path.abspath(__file__))
        # get the attached file full path.
        attach_file_path = current_path + '/' + attach_file_name
        # write attached file content to the file.
        with open(attach_file_path,'wb') as f:
            f.write(attach_file_data)

        print('attached file is saved in path ' + attach_file_path)

    else:
        content = msg.as_string()
        print(content)
