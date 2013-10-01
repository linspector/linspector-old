"""
A HTTPS backend to the current Linspector instance.

A Webserver listening for requests to give information about the internal state of linspector.
(maybe providing a JSON API to the instance too...)
"""

from lib.backends.backend import Backend


class HttpsBackend(Backend):
    def __init__(self, **kwargs):
        return