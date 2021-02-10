import json


class ReportSocial:

    def __init__(self, report_foto,
                 dictionary_parolechiave_nel_post,quantita_post_neltempo,social,valutazione_foto,valutazione_keywords,
                 nome):
        self.report_foto = report_foto
        self.dictionary_parolechiave_nel_post = dictionary_parolechiave_nel_post
        self.quantita_post_neltempo = quantita_post_neltempo
        self.social = social
        self.valutazione_foto = valutazione_foto
        self.valutazione_keywords = valutazione_keywords
        self.nome=nome

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
