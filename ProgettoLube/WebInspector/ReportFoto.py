import json


class ReportFoto:

    def __init__(self, correttezza_logo, competitors,presenza_scritte_foto):
        self.correttezza_logo = correttezza_logo
        self.competitors = competitors
        self.presenza_scritte_foto = presenza_scritte_foto

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=3)
