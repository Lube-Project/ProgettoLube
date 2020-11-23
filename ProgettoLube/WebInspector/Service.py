from Crawler import Crawler
from Report import Report


class Service:

    def valuta(self, sito):
        crawler = Crawler()
        report_pagine = crawler.generate_reportpagine(sito)
        # TODO: generazione report foto
        # TODO: cancellare directory foto
        report = Report(sito, report_pagine, None)
        return report
