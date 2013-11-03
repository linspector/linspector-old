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
import time

from email.mime.text import MIMEText
from logging import getLogger

from linspector.tasks.task import Task

logger = getLogger(__name__)


class MailTask(Task):
    def __init__(self, **kwargs):
        mandatory_args = ["host", "password", "from", "username"]
        for arg in mandatory_args:
            if not arg in kwargs:
                self.raise_config_exception(kwargs, arg)
        self.host = kwargs["host"]
        self.password = kwargs["password"]
        self.fromName = kwargs["from"]
        self.userName = kwargs["username"]
        self.port = 25
        if "port" in kwargs:
            self.port = kwargs["port"]

        #self.set_task_type(kwargs["type"])
        #self.recipient = kwargs["args"]["rcpt"]

    def execute(self, msg, taskArgs):
        #time.sleep(3)
        if "rcpt" not in taskArgs:
            logger.debug("Could not execute Mail Task! No recipient given!")
            raise "Could not execute Mail Task! No recipient given!"

        logger.debug("Eecuting Task!")

        message = MIMEText(msg)
        message['Subject'] = msg
        now = datetime.datetime.now()
        message['Date'] = now.strftime("%a, %d %b %Y %H:%M:%S")
        message['From'] = self.fromName
        message['To'] = taskArgs["rcpt"]
        s = smtplib.SMTP(self.host, self.port)
        #s.login(self.userName, self.password)
        s.sendmail(self.fromName, taskArgs["rcpt"], message.as_string())
        s.quit()


def create(taskDict):
    return MailTask(**taskDict)