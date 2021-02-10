import json


class Report:

    def __init__(self, sito, report_pagine, report_foto, valutazione_script, valutazione_foto,valutazione_keywords):
        self.sito = sito
        self.report_pagine = report_pagine
        self.report_foto = report_foto
        self.valutazione_script = valutazione_script
        self.valutazione_foto = valutazione_foto
        self.valutazione_keywords = valutazione_keywords

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=6)



