class Parser:
    def __init__(self, **kwargs):
        pass

    def parse_data(self, data):
        self.pre_parse(data)
        return self.generate_parse_result(data)
  
    def pre_parse(self, data):
        pass
    
    def generate_parse_result(self, result):
        pass