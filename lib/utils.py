import uuid
from bs4 import BeautifulSoup
from lib.email import Exchange

_xss_tags_whitelist = {
    'p': [],
    'i': [],
    'b': [],
    'a': ['href', 'title', 'target'],
    'h1': [],
    'h2': [],
    'h3': [],
    'h4': [],
    'h5': [],
    'tr': [],
    'td': [],
    'th': [],
    'em': [],
    'hr': [],
    'br': [],
    'ol': [],
    'ul': [],
    'li': [],
    'img': ['src', 'alt'],
    'del': [],
    'pre': [],
    'code': [],
    'span': [],
    'table': [],
    'thead': [],
    'tbody': [],
    'tfoot': [],
    'strong': [],
    'codespan': [],
    'blockquote': [],
}

_xss_values_blacklist = [
    'javascript'
]


class Utils:
    __mailer = None

    def __init__(self):
        self.__mailer = Exchange()

    def get_mailer(self):
        return self.__mailer

    @staticmethod
    def uuid_mapped(name):
        return uuid.uuid5(uuid.NAMESPACE_X500, name)

    @staticmethod
    def uuid_unmapped():
        return uuid.uuid1()

    @staticmethod
    def is_fetch_done(total: int, offset: int, limit: int):
        return (offset + limit) >= total

    @staticmethod
    def xss_filter(content: str):
        soup = BeautifulSoup(content, 'html.parser')
        for tag in soup.find_all():
            if tag.name in _xss_tags_whitelist:
                pass
            else:
                tag.hidden = True
                tag.clear()
                continue

            input_attrs = tag.attrs
            valid_attrs = _xss_tags_whitelist[tag.name]

            for k in list(input_attrs.keys()):
                if k in valid_attrs:
                    for v in _xss_values_blacklist:
                        if tag.attrs[k].find(v) != -1:
                            del tag.attrs[k]
                else:
                    del tag.attrs[k]
        return soup.decode()
