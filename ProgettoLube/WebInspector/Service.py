from Crawler import Crawler
from ImageWorker import ImageWorker
from Report import Report


class Service:

    def valuta(self, sito):
        crawler = Crawler()
        img_worker = ImageWorker()
        report_pagine = crawler.generate_reportpagine(sito)
        # TODO: generazione report foto
        report_foto = img_worker.generate_reportfoto()
        # TODO: cancellare directory foto
        report = Report(sito, report_pagine, report_foto)
        return report
