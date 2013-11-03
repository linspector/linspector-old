"""
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

from logging import getLogger

KEY_PARSER    = "parser"
KEY_COMMENT   = "comment"
KEY_THRESHOLD = "threshold"
KEY_FAILS     = "fails"
KEY_PERIODS   = "periods"
KEY_ARGS      = "args"

logger = getLogger(__name__)


class Service(object):
    def __init__(self, **kwargs):

        self._args = {}
        if KEY_ARGS in kwargs:
            self.add_arguments(kwargs[KEY_ARGS])
        elif self.needs_arguments():
            raise Exception("Error: needs arguments but none provided!")

        self._parser = []
        if KEY_PARSER in kwargs:
            self.add_parser(kwargs[KEY_PARSER])
        
        self._comment = None
        if KEY_COMMENT in kwargs:
            self._comment = kwargs[KEY_COMMENT]    
        
        self._threshold = 0
        if KEY_THRESHOLD in kwargs:
            self._threshold = kwargs[KEY_THRESHOLD]
        
        self._fails = {}        
        if KEY_FAILS in kwargs:
            self.put_fails(kwargs[KEY_FAILS])

        self._periods = []
        if KEY_PERIODS in kwargs:
            self.add_periods(kwargs[KEY_PERIODS])

    def __str__(self):
        return self.get_name() + " " + repr(self._args)

    def get_type(self):
        return str(self.__class__)

    def get_name(self):
        return self.__class__.__name__

    def add_arguments(self, args):
        for key, val in args.items():
            self._args[key] = val
            
    def add_argument(self, key, value):
        self._args[key] = value
        
    def get_arguments(self):
        return self._args

    def add_periods(self, period):
        if period is not None:
            if isinstance(period, list):
                self._periods.extend(period)
            else:
                self._periods.append(period)

    def set_hostgroup(self, hostgroup):
        self.hostgroup = hostgroup

    def get_hostgroup(self):
        return self.hostgroup
    
    def get_periods(self):
        return self._periods
    
    def get_fails(self):
        return self._fails
    
    def has_fail(self, fail):
        return fail in self.get_fails()
    
    def put_fail(self, key, value):
        self._fails[key] = value
        
    def put_fails(self, fails):
        for key, value in fails.items():
            self.put_fail(key, value)

    def get_threshold(self):
        return self._threshold
    
    def get_comment(self):
        return self._comment
    
    def get_parser(self):
        return self._parser

    def add_parser(self, parser):
        if parser is not None:
            if isinstance(parser, list):
                self._parser.extend(parser)
            else:
                self._parser.append(parser)
                
    def needs_arguments(self):
        return False

    def _execute(self, jobInfo):
        try:
            self.pre_execute(jobInfo)

            self.execute(jobInfo)
            self.parse_result(jobInfo)
            self.post_execute(jobInfo)
        except Exception, e:
            self.set_execution_successful(False)
            self._threshold -= 1
            raise e

    def execute(self, jobInfo):
        pass

    def pre_execute(self, jobInfo):
        pass

    def parse_result(self, jobInfo):

        result = []
        for parser in self.get_parser():
            result.append(parser.parse(jobInfo))

        return result

    def post_execute(self, jobInfo):
        pass