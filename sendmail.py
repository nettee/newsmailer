#!/usr/bin/env python3

import configparser

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr

import smtplib

config = configparser.ConfigParser()
config.read('mail.ini')
from_name = '大萌萌新鲜推送'
from_addr = config['sender']['address']
password = config['sender']['password']
smtp_server = config['sender']['server']

def format_addr(name, addr):
    return formataddr((Header(name, 'utf-8').encode(), addr))

def sendmail(mail, receiver):
    mimetype = mail['mimetype']
    subject = mail['subject']
    body = mail['body']

    msg = MIMEMultipart()
    msg['From'] = format_addr(from_name, from_addr)
    msg['To'] = receiver
    msg['Subject'] = Header(subject, 'utf-8').encode()
    msg.attach(MIMEText(body, mimetype, 'utf-8'))
    server = smtplib.SMTP(smtp_server, 25)
    server.login(from_addr, password)
    server.sendmail(from_addr, [receiver], msg.as_string())
    server.quit()
