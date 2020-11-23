import json


class ReportPagine:

    def __init__(self, lista_href, dictionary_script, dictionary_parolechiave):
        self.lista_href = lista_href
        self.dictionary_script = dictionary_script
        self.dictionary_parolechiave = dictionary_parolechiave

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=3)
