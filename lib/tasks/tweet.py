"""
The tweet/twitter task.
"""

import twitter
from lib.tasks.task import Task


class TweetTask(Task):
    def __init__(self, **kwargs):
        if not "type" in kwargs:
            raise Exception("'type' not in typeDict " + str(kwargs))
        if not "args" in kwargs:
            raise Exception("typeDict " + str(kwargs) + " has no arguments!")
        self.set_task_type(kwargs["type"])
        self.recipient = kwargs["args"]["rcpt"]

    def execute(self, msg):
        api = twitter.Api(consumer_key='consumer_key',
                          consumer_secret='consumer_secret',
                          access_token_key='access_token',
                          access_token_secret='access_token_secret')
        status = api.PostUpdate(msg)
        pass


def create(taskDict):
    return TweetTask(**taskDict)