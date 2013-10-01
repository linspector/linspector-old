"""
Frontends are GUI interfaces to Linspector. This could be a shell or other terminal based GUI.

Frontends are absolutely no requirement for running Linspector. If no frontend is selected Linspector will just log
stuff to stdout.
"""


class Frontend():
    def __init__(self, **kwargs):
        return