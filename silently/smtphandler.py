#!/usr/bin/env python

import logging
import logging.handlers
import smtplib
from datetime import datetime
from email.mime.text import MIMEText

from werkzeug.debug.repr import DebugReprGenerator

EMAIL_LIMIT = 1000

class EmailErrorHandler(object):
    """Convenience class for init_app like behavior.

    This error handler should be moved to its own repo so it can be reused
    across projects.
    """

    def init_app(self, app):
        """Registers an SMTP logging handler on the app.

        Args:
            app: A flask app.
        """
        mail_handler = BufferingSMTPHandler(app.config['SMTP_SERVER'],
                                            app.config['SMTP_USERNAME'],
                                            app.config['SMTP_PASSWORD'],
                                            app.config['SMTP_FROM'],
                                            app.config['ERROR_EMAIL_ADDRESS'],
                                            app.config['ERROR_EMAIL_SUBJECT'],
                                            app.config['SMTP_BUFFER_LENGTH'])
        formatter = logging.Formatter('%(asctime)s ' +
                '- %(filename)s - %(lineno)d - %(levelname)s\n\n%(message)s')
        mail_handler.setFormatter(formatter)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


class BufferingSMTPHandler(logging.handlers.BufferingHandler):
    """Buffered SMTP logging handler.

    This is meant to be used for severe errors where the admin should be
    notified that a server is in poor health.
    """
    _last_emit = None
    _debug = DebugReprGenerator()
    _counter = 0

    def __init__(self, mailhost, username, password, fromaddr, toaddrs,
            subject, capacity):
        super(BufferingSMTPHandler, self).__init__(capacity)
        self.mailhost = mailhost
        self.mailport = None
        self.username = username
        self.password = password
        self.fromaddr = fromaddr
        self.toaddrs = toaddrs
        self.subject = subject


    def flush(self):
        """Sends a concatenated list of errors."""
        if self._counter > EMAIL_LIMIT:
            raise Exception('Error email limit of %s exceeded' % (EMAIL_LIMIT,))

        ready_to_flush = not self._last_emit or \
                (datetime.now() - self._last_emit).seconds > 60
        if len(self.buffer) > 0 and ready_to_flush:
            try:
                body = ''
                for record in self.buffer:
                    body = body + self.format(record) + "\r\n"
                msg = MIMEText(body)
                msg['Subject'] = 'Silently Error Hanlder %s' % (
                    datetime.now().strftime('%Y-%m-%d %H:00'))
                msg['From'] = self.fromaddr
                msg['To'] = ','.join(self.toaddrs)
                smtp = smtplib.SMTP(self.mailhost, smtplib.SMTP_PORT)
                smtp.ehlo() # for tls add this line
                smtp.starttls() # for tls add this line
                smtp.ehlo() # for tls add this line
                smtp.login(self.username, self.password)
                msg.set_payload(body)
                smtp.sendmail(self.fromaddr, self.toaddrs, msg.as_string())
                smtp.quit()
                self._last_emit = datetime.now()
                self._counter += 1
            except:
                raise
            self.buffer = []
