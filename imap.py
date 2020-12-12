
import imaplib
import email

def check_mail_imap(user_name,password,counter,dele):
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
    print('Server :',ser_sta)
    print('Server :',ser_res[0].decode('utf-8'))
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
if __name__=='__main__':
    user_name = 'remitai1998@gmail.com'
    password = '10111998tai'
    counter = -2
    dele  = False
    print('Server : \n',check_mail_imap(user_name,password,counter,dele))
