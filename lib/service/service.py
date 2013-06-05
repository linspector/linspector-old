class Service:
    def __init__(self, host, parser):
        self.host = host
        self.parser = parser
        self.errorcode = 0
        self.errormessage = "No Error!"

    def _execute(self):
        self.pre_execute()
        self.execute()
        self.parse_result()
        self.handle_result()

    def execute(self):
        pass

    def pre_execute(self):
        pass

    def parse_result(self):
        self.parser._parse()

    def handle_result(self):
        pass