import sys, os

from exchangelib import *

from config.mail import ExchangeConfig, Template


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

    def send(self, mailto: str, fields: dict, template: Template):
        with open('template/email/%s.temp.html' % template.value, encoding='utf-8') as fs:
            mail = fs.read()
            for k, v in fields.items():
                mail = mail.replace('{%s}' % k, v)
        msg = Message(
            account=self._account,
            subject='评论有新的回复！',
            body=HTMLBody(mail),
            to_recipients=[Mailbox(email_address=mailto)],
        )
        msg.send()
