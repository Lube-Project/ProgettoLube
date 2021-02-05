import json


class ReportSocial:

    def __init__(self, report_foto,
                 dictionary_parolechiave_nel_post,quantità_post_neltempo,social):
        self.report_foto = report_foto
        self.dictionary_parolechiave_nel_post = dictionary_parolechiave_nel_post
        self.quantità_post_neltempo = quantità_post_neltempo
        self.social = social

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
