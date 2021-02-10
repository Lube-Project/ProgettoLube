import json


class ReportFoto:

    def __init__(self, correttezza_logo,presenza_keywords_foto):
        self.correttezza_logo = correttezza_logo
        self.presenza_keywords_foto = presenza_keywords_foto

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=2)
