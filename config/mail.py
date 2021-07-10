from enum import Enum


class Template(Enum):
    TEMPLATE_REPLY = 'reply'
    TEMPLATE_MENTION = 'mention'


class Protocol(Enum):
    EXCHANGE = 'exchange'
    SMTP = 'smtp'


class MailConfig:
    protocol = Protocol.SMTP


class ExchangeConfig:
    host = 'ibox.moe'
    email = 'ovo-noreply@ibox.moe'
    password = 'Rf8jUabvWWCSi5m'


class SMTPConfig:
    host = 'smtp.office365.com'
    port = 587
    email = 'ovo-noreply@ibox.moe'
    password = 'Rf8jUabvWWCSi5m'
