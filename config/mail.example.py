from enum import Enum


class ExchangeConfig:
    host = 'MAIL_SERVER'
    email = 'user@domain.com'
    password = 'xxxxxxxxxxx'


class Template(Enum):
    TEMPLATE_REPLY = 'reply'
