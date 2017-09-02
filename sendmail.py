#!/usr/bin/env python3

import configparser

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib

receiver = 'anchori@163.com'
#receiver = 'tfn0510@gmail.com'

config = configparser.ConfigParser()
config.read('mail.ini')
from_name = '大萌萌新鲜推送'
from_addr = config['sender']['address']
password = config['sender']['password']
smtp_server = config['sender']['server']

def format_addr(name, addr):
    return formataddr((Header(name, 'utf-8').encode(), addr))

def send_text(subject, text):
    msg = MIMEText(text, 'plain', 'utf-8')
    msg['From'] = format_addr(from_name, from_addr)
    msg['To'] = receiver
    msg['Subject'] = Header(subject, 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [receiver], msg.as_string())
    server.quit()

def sendmail(mail):
    mimetype = mail['mimetype']
    subject = mail['subject']
    text = mail['text']

    msg = MIMEText(text, mimetype, 'utf-8')
    msg['From'] = format_addr(from_name, from_addr)
    msg['To'] = receiver
    msg['Subject'] = Header(subject, 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [receiver], msg.as_string())
    server.quit()
