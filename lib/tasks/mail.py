"""
The email task.

http://docs.python.org/2/library/email-examples.html
"""

#import smtplib
#from email.mime.text import MIMEText
from lib.tasks.task import Task


class EmailTask(Task):
    def __init__(self, **kwargs):
        if not "type" in kwargs:
            raise Exception("'type' not in typeDict " + str(kwargs))
        if not "args" in kwargs:
            raise Exception("typeDict " + str(kwargs) + " has nor arguments!")
        self.set_task_type(kwargs["type"])
        self.recipient = kwargs["args"]["rcpt"]

    def execute(self, msg):
        '''
        message = MIMEText(msg)
        message['Subject'] = 'Warning from Linspector'
        message['From'] = "warning@linspector.org"
        message['To'] = self.recipient
        s = smtplib.SMTP('localhost')
        s.sendmail("warning@linspector.org", self.recipient, message.as_string())
        s.quit()
        '''

        print("Task executed")
        print(msg)
        print(self.recipient)
        pass


def create(taskDict):
    return EmailTask(**taskDict)