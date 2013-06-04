
class Service:
    def __init__(self):
        pass

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
        pass

    def handle_result(self):
        pass