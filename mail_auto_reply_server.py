# coding: utf-8
import smtpd
import asyncore
from utils.logger import logger as log
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
            body=mcp.content,
            raw_data=data
        )


class MailAutoReplyServer(object):

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
