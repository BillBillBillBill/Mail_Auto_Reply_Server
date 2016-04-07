# coding: utf-8
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr


class MailContentParser(object):

    def __init__(self, data):
        self.data = Parser().parsestr(data)
        self.d = {}
        self.text = []
        self.attachs = []
        self.parse_data(self.data)

    def __getitem__(self, key):
        return self.d[key]

    def __setitem__(self, key, value):
        self.d[key] = value

    def parse_data(self, msg, is_sub_obj=False):
        if is_sub_obj == 0:
            # 邮件的From, To, Subject存在于根对象上:
            for header in ['From', 'To', 'Subject']:
                value = msg.get(header, '')
                if value:
                    if header == 'Subject':
                        # 需要解码Subject字符串:
                        value = self.decode_str(value)
                    else:
                        # 需要解码Email地址:
                        hdr, addr = parseaddr(value)
                        value = u'%s' % addr
                self[header] = value
        if (msg.is_multipart()):
            # 如果邮件对象是一个MIMEMultipart,
            # get_payload()返回list，包含所有的子对象:
            parts = msg.get_payload()
            for n, part in enumerate(parts):
                # print('%spart %s' % ('  ' * indent, n))
                # print('%s--------------------' % ('  ' * indent))
                # 递归解析每一个子对象:
                self.parse_data(part, True)
        else:
            # 邮件对象不是一个MIMEMultipart,
            # 就根据content_type判断:
            content_type = msg.get_content_type()
            if content_type == 'text/plain' or content_type == 'text/html':
                # 纯文本或HTML内容:
                content = msg.get_payload(decode=True)
                # 要检测文本编码:
                charset = self.guess_charset(msg)
                if charset:
                    content = content.decode(charset)
                self.text.append(("Text", content))
            else:
                # 不是文本,作为附件处理:
                content = msg.get_payload()
                self.attachs.append((content_type, content))

    def decode_str(self, s):
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value

    def guess_charset(self, msg):
        # 先从msg对象获取编码:
        charset = msg.get_charset()
        if charset is None:
            # 如果获取不到，再从Content-Type字段获取:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        return charset
