# -*- coding: utf-8 -*-

import smtpd
import asyncore
import logging as log
from email.parser import Parser
from utils.mail_content_parser import MailContentParser



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

        log.warn('Starting SMTP server at {0}:{1}'.format(address, port))

        MailboxServer(self.collator, (address, port), None)

        try:
            asyncore.loop()
        except KeyboardInterrupt:
            log.info('Cleaning up')


if __name__ == '__main__':

    marserv = MailAutoReplyServer()

    @marserv.collate
    def handler(to, sender, subject, body):
        print "收件人：", to
        print "发件人：", sender
        print "标题：", subject
        print body

    # Bind directly.
    marserv.serve(address='0.0.0.0', port=25)
