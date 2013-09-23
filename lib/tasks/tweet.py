"""
The tweet/twitter task.

Uses: tweepy
"""

import tweepy
from lib.tasks.task import Task


class TweetTask(Task):
    def __init__(self, **kwargs):
        if not "type" in kwargs:
            raise Exception("'type' not in typeDict " + str(kwargs))
        if not "args" in kwargs:
            raise Exception("typeDict " + str(kwargs) + " has no arguments!")
        self.set_task_type(kwargs["type"])
        self.recipient = kwargs["args"]["rcpt"]

    def execute(self, msg, core):
        auth = tweepy.BasicAuthHandler("user", "pass")
        api = tweepy.API(auth)
        api.update_status(self.recipient)
        print(self.get_task_type())


def create(taskDict):
    return TweetTask(**taskDict)