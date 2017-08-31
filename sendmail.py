#!/usr/bin/env python3

import configparser

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib

def format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

config = configparser.ConfigParser()
config.read('mail.ini')
from_name = config['sender']['name']
from_addr = config['sender']['address']
password = config['sender']['password']
smtp_server = config['sender']['server']
to_name = config['receiver']['name']
to_addr = config['receiver']['address']

#from_addr = input('From: ')
#password = input('Password: ')
#to_addr = input('To: ')
#smtp_server = input('SMTP server: ')

#msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
html = '''<html><body>
<h1>Hello</h1>
<p>send by Damengmeng</p>
</body></html>'''
msg = MIMEText(html, 'html', 'utf-8')
msg['From'] = format_addr('{} <{}>'.format(from_name, from_addr))
msg['To'] = format_addr('{} <{}>'.format(to_name, to_addr))
msg['Subject'] = Header('来自大萌萌的问候', 'utf-8').encode()

server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
