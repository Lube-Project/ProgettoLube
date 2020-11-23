import json


class Report:

    def __init__(self, sito, report_pagine, report_foto):
        self.sito = sito
        self.report_pagine = report_pagine
        self.report_foto = report_foto

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=3)



