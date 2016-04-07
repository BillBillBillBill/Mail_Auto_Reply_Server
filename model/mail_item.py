# coding: utf-8
from conn import m


class MailItem(m.Document):
    sender = m.StringField(required=True)
    to = m.StringField(required=True)
    subject = m.StringField(required=True)
    content = m.StringField(required=True)
    attachs = m.StringField(required=False)
    raw_data = m.StringField(required=True)


class BadMailItem(m.Document):
    sender = m.StringField(required=True)
    to = m.StringField(required=True)
    subject = m.StringField(required=True)
    content = m.StringField(required=True)
    attachs = m.StringField(required=False)
    raw_data = m.StringField(required=True)
