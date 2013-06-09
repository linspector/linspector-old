class Service:
    def __init__(self, host, parser):
        self.host = host
        self.parser = parser
        self.errorcode = 0
        self.errormessage = "No Error!"

    def _execute(self):
        self.pre_execute()
        executionResult = self.execute()
        parseResult = self.parse_result(executionResult)
        self.handle_result(parseResult)

    def execute(self):
        pass

    def pre_execute(self):
        pass

    def parse_result(self, executionResult):
        return self.parser._parse(executionResult)

    def handle_result(self, parseResult):
        pass
