# -*- coding: utf-8 -*-
"""This module is the entry point for a celery worker."""

from flask import current_app
import smtplib
import os
from email.mime.text import MIMEText

celery = create_celery_app()

def celery_thread(f):
    def inner(*args, **kwargs):
        return gevent.spawn(copy_current_app_context(f), *args, **kwargs)
    return inner

@celery.task()
def hello_world():
    return "hello world"

@celery.task
def sendmail(to_addr=None, from_address=None, from_name=None,
             subject=None, body=None):

    username = os.getenv['SMTP_USERNAME']
    password = os.getenv['SMTP_PASSWORD']
    server = os.getenv['SMTP_SERVER']
    domain = os.getenv['SMTP_DOMAIN']

    port = 465
    smtp_service = smtplib.SMTP_SSL(server, port, domain)

    msg = MIMEText(body, 'html')
    msg['From'] = '"%s" <%s>' % (from_name, from_address)
    msg['To'] = to_addr
    msg['Subject'] = subject

    smtp_service.set_debuglevel(0)
    smtp_service.login(username, password)
    smtp_service.sendmail(from_address, to_addr, msg.as_string())
