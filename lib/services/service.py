
KEY_PARSER    = "parser"
KEY_COMMENT   = "comment"
KEY_THRESHOLD = "threshold"
KEY_FAILS     = "fails"
KEY_PERIODS   = "periods"
KEY_ARGS      = "args"


class Service(object):
    def __init__(self, **kwargs):

        self._args = {}
        if KEY_ARGS in kwargs:
            self.add_arguments(kwargs[KEY_ARGS])
        elif self.needs_arguments():
            raise Exception("Error: needs arguments but none provided!")
        
        self._host = None
        
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
        
        self.errorcode = 0
        self.errormessage = None
        
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
    
    def set_host(self, host):
        self._host = host
        
    def get_host(self):
        return self._host
    
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

    def _execute(self):
        self.pre_execute()
        result = {}
        for host in self.get_hostgroup().get_hosts():
            result[host] = self.execute(host)

        parseResult = self.parse_result(result)
        self.handle_result(parseResult)

    def execute(self, host):
        pass

    def pre_execute(self):
        pass

    def parse_result(self, executionResult):
        result = []
        for parser in self.get_parser():
            result.append(parser.parse(executionResult))

    def handle_result(self, parseResult):
        pass