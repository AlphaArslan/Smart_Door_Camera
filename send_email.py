#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib, ssl
import email.mime.text

SMTP_PORT = 465  # For SSL
SMTP_SERVER = "smtp.gmail.com"
_SENDER_EMAIL = "dev.script.21@gmail.com"
_SENDER_PASS = "0.9millidev"
EMAIL_CONTENT = """\
Subject: Smart Camera System Alarm

There is an unauthorized person at the door.
Manual Control : {}
Authorize people : {}
""".format("http://192.168.1.5:5000/stream", "http://192.168.1.5:5000/users")


class Email():
    def __init__(self, sender_mail, sender_pass):
        self.sender = sender_mail
        self.context = ssl.create_default_context()
        self.server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=self.context)
        self.server.login(sender_mail, sender_pass)

    def send_mail(self, receiver_mail, content):
        msg = content
        # msg = email.mime.text.MIMEText(content, _charset="UTF-8").as_string()
        self.server.sendmail(self.sender, receiver_mail, msg)

def send_default_msg():
    e = Email(_SENDER_EMAIL, _SENDER_PASS)
    e.send_mail("cugcom@gmail.com", EMAIL_CONTENT)

#########################################
if __name__ == '__main__':
    send_default_msg()
