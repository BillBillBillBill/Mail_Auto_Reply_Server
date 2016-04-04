# coding: utf-8
import smtpd
import asyncore
import re
import requests
import json
from utils.logger import logger as log
from utils.mail_content_parser import MailContentParser


separator1 = "------------------------------------------------------------"
separator2 = "============================================================"


class MailboxServer(smtpd.SMTPServer, object):
    """Logging-enabled SMTPServer instance with handler support."""

    def __init__(self, handler, *args, **kwargs):
        super(MailboxServer, self).__init__(*args, **kwargs)
        self._handler = handler

    def process_message(self, peer, mailfrom, rcpttos, data):
        mcp = MailContentParser(data)
        return self._handler(
            to=mcp["To"],
            sender=mcp["From"],
            subject=mcp["Subject"],
            body=mcp.content
        )


class MailAutoReplyServer(object):
    """A simple SMTP Inbox."""

    def __init__(self, port=None, address=None):
        self.port = port
        self.address = address
        self.collator = None

    def collate(self, collator):
        """Function decorator. Used to specify inbox handler."""
        self.collator = collator
        return collator

    def serve(self, port=None, address=None):
        """Serves the SMTP server on the given port and address."""
        port = port or self.port
        address = address or self.address

        log.info(u'Starting SMTP server at {0}:{1}'.format(address, port))

        MailboxServer(self.collator, (address, port), None)

        try:
            asyncore.loop()
        except KeyboardInterrupt:
            log.info(u'Cleaning up')


if __name__ == '__main__':

    marserv = MailAutoReplyServer()

    @marserv.collate
    def handler(to, sender, subject, body):
        try:
            content = u"收件人：%s\n发件人：%s\n标题：%s\n 内容：%s" % (to, sender, subject, json.dumps(body))
            log.info(content)
            log.info(separator1*4)

            urls = []
            for content in body:
                if content[0] == 'Text':
                    # find all url
                    urls += re.findall('href="(http://.*?)"', content[1])
            log.info(u"发现%d个链接" % len(urls))
            # open them
            for url in urls:
                try:
                    ret = requests.get(url)
                    status = ret.status_code
                except Exception, e:
                    status = e.message
                log.info(u"url: %s  status: %s" % (url, status))
            log.info(separator2*4)
        except Exception, e:
            log.error(e.message)

    # Bind directly.
    marserv.serve(address='0.0.0.0', port=25)
