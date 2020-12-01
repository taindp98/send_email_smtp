import base64
from socket import *
import ssl
import poplib
import imaplib
import email

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
    rcpContent = f'RCPT TO: <{receiver}>'
    mailCommand = "{}\r\n".format(rcpContent).encode()
    clientSocket.send(mailCommand)
    print('Client :',rcpContent)
    recv1 = clientSocket.recv(1024).decode()
    print('Server :',recv1)
    if recv1[:3] != '250':
        print('250 reply not received from server.')
    dataContent = 'DATA'
    dataCommand = '{}\r\n'.format(dataContent).encode()
    clientSocket.send(dataCommand)
    print('Client :',dataContent)
    recv1 = clientSocket.recv(1024).decode()
    print('Server :',recv1)
    if recv1[:3] != '354':
        print('data 354 reply not received from server.')
    mess = f'{message}\r\n.\r\n'
    clientSocket.send(mess.encode())
    print('Client :', mess)
    recv1 = clientSocket.recv(1024).decode()
    print('Server :',recv1)
    if recv1[:3] != '250':
        print('end msg 250 reply not received from server.')
    quitContent = 'QUIT'
    quitCommand = '{}\r\n'.format(quitContent).encode()
    clientSocket.send(quitCommand)
    print('Client :', quitContent)
    recv1 = clientSocket.recv(1024).decode()
    print('Server :',recv1)
    if recv1[:3] != '221':
        print('quit 221 reply not received from server.')
def send_email(user_name,password,host,port,message,receiver):
    clientSocket = socket(AF_INET,SOCK_STREAM)
    clientSocket.connect((host, port))
    context = ssl.create_default_context()
    clientSocket = context.wrap_socket(clientSocket, server_hostname=host)
    authorization_login(user_name,password,clientSocket,message,receiver)

def check_mail_pop3(user_name,password,host,port):
    server = poplib.POP3_SSL(host, port)
    print('Server :',server.getwelcome().decode('utf-8'))
    server.user(user_name)
    print('Client : user',user_name)
    server.pass_(password)
    print('Server :',server.retr(1)[0].decode('utf-8'))
    print('Client : list')
    resp, mails, octets = server.list()
    print('Server :', len(mails))
    # print(mails)
    # print('Server :',resp.decode('utf-8'))
    index = len(mails)
    print('Client : retr',index)
    msg = server.retr(index)
    response = msg[0]
    # print('Server :',response.decode('utf-8'))
    lines = msg[1]
    octets = msg[2]
    msg_content = b'\r\n'.join(lines).decode('utf-8')
    print('Server :',msg_content)
    print('Client : quit')
    # server.quit()
    print('Server : +OK POP3 server signing off')
    return msg_content

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


