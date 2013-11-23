"""
The mail task.

http://docs.python.org/2/library/email-examples.html#

Copyright (c) 2011-2013 by Johannes Findeisen and Rafael Timmerberg

This file is part of Linspector (http://linspector.org).

Linspector is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import datetime
import smtplib

from email.mime.text import MIMEText
from logging import getLogger

from linspector.tasks.task import Task

logger = getLogger(__name__)


class MailTask(Task):
    def __init__(self, **kwargs):
        super(MailTask, self).__init__(**kwargs)

        args = self.get_arguments()

        if "sender" in args:
            self.sender = args["sender"]
        else:
            raise Exception("There is no sender set")

        if "rcpt" in args:
            self.rcpt = args["rcpt"]
        else:
            raise Exception("There is no rcpt set")

        self.host = "localhost"
        if "host" in args:
            self.host = args["host"]

        self.port = 25
        if "port" in args:
            self.port = args["port"]

        self.username = None
        if "username" in args:
            self.username = args["username"]

        self.password = None
        if "password" in args:
            self.password = args["password"]

    def needs_arguments(self):
        return True

    def execute(self, job_information):
        logger.debug("Executing Mail Task!")

        message = MIMEText(job_information.get_response_message())
        message['Subject'] = job_information.get_response_message()
        now = datetime.datetime.now()
        message['Date'] = now.strftime("%a, %d %b %Y %H:%M:%S")
        message['From'] = self.sender
        message['To'] = self.rcpt

        s = smtplib.SMTP(self.host, self.port)

        if self.username and self.password:
            try:
                s.login(self.username, self.password)
            except Exception, e:
                logger.error(e)

        s.sendmail(self.sender, self.rcpt, message.as_string())
        s.quit()


def create(kwargs):
    return MailTask(**kwargs)