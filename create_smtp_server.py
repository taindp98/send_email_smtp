import smtpd
import threading
import asyncore
from utils import *
server = smtpd.SMTPServer(('localhost', 12345), None)
print(server)
loop_thread = threading.Thread(target=asyncore.loop, name="Asyncore Loop")
print(loop_thread)
loop_thread.daemon = True
loop_thread.start()
