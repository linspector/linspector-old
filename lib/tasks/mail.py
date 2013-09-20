"""
The mail task.

http://docs.python.org/2/library/email-examples.html
"""

import datetime
import smtplib
from email.mime.text import MIMEText
from lib.tasks.task import Task


class MailTask(Task):
    def __init__(self, **kwargs):
        if not "type" in kwargs:
            raise Exception("'type' not in typeDict " + str(kwargs))
        if not "args" in kwargs:
            raise Exception("typeDict " + str(kwargs) + " has no arguments!")
        self.set_task_type(kwargs["type"])
        self.recipient = kwargs["args"]["rcpt"]

    def execute(self, msg, core):
        message = MIMEText(msg)
        message['Subject'] = msg
        now = datetime.datetime.now()
        message['Date'] = now.strftime("%a, %d %b %Y %H:%M:%S")
        message['From'] = core["tasks"]["mail"]["from"]
        message['To'] = self.recipient
        s = smtplib.SMTP(core["tasks"]["mail"]["host"], core["tasks"]["mail"]["port"])
        s.sendmail(core["tasks"]["mail"]["from"], self.recipient, message.as_string())
        s.quit()


def create(taskDict):
    return MailTask(**taskDict)