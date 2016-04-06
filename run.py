# coding: utf-8
import re
import requests
import json
from mail_auto_reply_server import MailAutoReplyServer
from utils.logger import logger as log
from model.mail_item import MailItem

separator1 = "------------------------------------------------------------"
separator2 = "============================================================"


marserv = MailAutoReplyServer()

@marserv.collate
def handler(to, sender, subject, body, raw_data):
    try:
        content = u"收件人：%s\n发件人：%s\n标题：%s\n 内容：%s" % \
                (to, sender, subject, json.dumps(body))
        mail_item = MailItem(sender, to, subject, json.dumps(body), raw_data)
        mail_item.save()
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