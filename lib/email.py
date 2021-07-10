import sys, os

from exchangelib import *

import smtplib
from email.mime.text import MIMEText
from email.header import Header

from config.mail import MailConfig, ExchangeConfig, SMTPConfig, Protocol, Template


class Exchange:
    _config = ExchangeConfig

    _credentials = None
    _account = None

    def __init__(self):
        self._creds = Credentials(
            username=self._config.email,
            password=self._config.password
        )
        self.config = Configuration(
            server=self._config.host,
            credentials=self._creds
        )
        self._account = Account(
            primary_smtp_address=self._config.email,
            autodiscover=True,
            config=self.config,
            access_type=DELEGATE
        )

    async def send(self, mailto: str, fields: dict, template: Template, subject: str = 'OvO Notification'):
        with open('template/email/%s.temp.html' % template.value, encoding='utf-8') as fs:
            mail = fs.read()
            for k, v in fields.items():
                mail = mail.replace('{%s}' % k, v)
        msg = Message(
            account=self._account,
            subject=subject,
            body=HTMLBody(mail),
            to_recipients=[Mailbox(email_address=mailto)],
            bcc_recipients=[Mailbox(email_address='boxlab@foxmail.com')],
        )
        msg.send()


class SMTP:
    _config = SMTPConfig
    _smtp = None

    def __init__(self):
        self._smtp = smtplib.SMTP(self._config.host, self._config.port)
        self._smtp.starttls()
        self._smtp.login(self._config.email, self._config.password)

    async def send(self, mailto: str, fields: dict, template: Template, subject: str = 'OvO Notification'):
        with open('template/email/%s.temp.html' % template.value, encoding='utf-8') as fs:
            mail = fs.read()
            for k, v in fields.items():
                mail = mail.replace('{%s}' % k, v)
        message = MIMEText(mail, 'html', 'utf-8')
        message['To'] = Header(mailto, 'utf-8')
        message['Subject'] = Header(subject, 'utf-8')
        try:
            self._smtp.sendmail(self._config.email, mailto, message.as_string())
        except smtplib.SMTPException:
            print('Error when sending mail')


class MailController:
    _engine = None

    def __init__(self):
        if self._engine is None:
            if MailConfig.protocol == Protocol.EXCHANGE:
                self._engine = Exchange()
            elif MailConfig.protocol == Protocol.SMTP:
                self._engine = SMTP()

    def get_mail_engine(self):
        return self._engine
