
import poplib
import os
from datetime import datetime

def check_mail_pop3(user_name,password):
    path_save = '/home/taindp/PycharmProjects/email/download_pop3'
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S").replace(r'/',r'_').replace(r':',r'_').replace(r' ',r'_')
    name_save = os.path.join(path_save,dt_string)
    # print(dt_string)
    host = 'pop.gmail.com'
    port = '995'
    server = poplib.POP3_SSL(host, port)
    print('-----Authorization-----')
    print('Server :',server.getwelcome().decode('utf-8'))
    server.user(user_name)
    print('Client : user',user_name)
    print('Server :', server.user(user_name).decode('utf-8'))
    # server.pass_(password)
    print('Client : pass','******')
    print('Server :', server.pass_(password).decode('utf-8'))
    # try:


        # (messageCount, totalMessageSize) = server.stat()
        # print('Server : {} messages in Mailbox'.format(messageCount))
        # print('Server : {} total messages size bytes'.format(totalMessageSize))
    print('-----Transaction-----')
    resp, mails, octets = server.list()
    if mails:
        print('Client : list')
        print('Server :',server.retr(1)[0].decode('utf-8'))

        print('Server :',resp.decode('utf-8'))
        index = len(mails)
        if index > 0:
            # file_save = open(name_save,'w')
            for item in range(0,index):
                file_save = open(str(name_save+'_'+str(item)+'.txt'),'w')
                msg = server.retr(item+1)[1]

                for m in msg:
                    if m.decode('utf-8').startswith('Subject'):
                        print ('\t' + m.decode('utf-8'))
                msg_text = b'\r\n'.join(msg).decode('utf-8')
                # print(parse_email_header(msg_text))
                file_save.write(msg_text)
                server.dele(item+1)
            server.quit()
        else:
            server.quit()
    else:
        print('Server : Mailbox empty')
if __name__ == '__main__':
    user_name = 'remitai1998@gmail.com'
    password = '10111998tai'
    check_mail_pop3(user_name,password)
