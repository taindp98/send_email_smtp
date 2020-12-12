import base64
from socket import *
import ssl

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
"""
CONNECTION ESTABLISHMENT
      S: 220
      E: 554
   EHLO or HELO
      S: 250
      E: 504, 550
   MAIL
      S: 250
      E: 552, 451, 452, 550, 553, 503
   RCPT
      S: 250, 251 (but see section 3.4 for discussion of 251 and 551)
      E: 550, 551, 552, 553, 450, 451, 452, 503, 550
   DATA
      I: 354 (Start adding mail input) -> data -> 
            S: 250
            E: 552, 554, 451, 452
      E: 451, 554, 503
   RSET
      S: 250
   VRFY
      S: 250, 251, 252
      E: 550, 551, 553, 502, 504
   EXPN
      S: 250, 252
      E: 550, 500, 502, 504
   HELP
      S: 211, 214
      E: 502, 504
   NOOP
      S: 250
   QUIT
      S: 221
"""
if __name__ == '__main__':
    user_name = 'remitai1998@gmail.com'
    password = '10111998tai'
    receiver = 'remitai1998@gmail.com'
    message = 'Hello world'
    send_email(user_name,password,message,receiver)
