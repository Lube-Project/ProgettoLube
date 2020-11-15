import json


class ReportFoto:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
