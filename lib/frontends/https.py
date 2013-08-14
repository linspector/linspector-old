"""
A HTTPS frontend to the current Linspector instance.

A Webserver listening for requests to give information about the internal state of linspector.
(maybe providing a JSON API to the instance too...)
"""

from lib.frontends.frontend import Frontend


class HttpsFrontend(Frontend):
    def __init__(self, **kwargs):
        return