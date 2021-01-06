from Crawler import Crawler
from ImageWorker import ImageWorker
from Report import Report


class Service:

    def valuta(self, sito):
        crawler = Crawler()
        img_worker = ImageWorker()
        report_pagine = crawler.generate_reportpagine(sito)
        # TODO: generazione report foto
        #report_foto = img_worker.generate_reportfoto()
        # TODO: cancellare directory foto
        #report = self.evaluate_report(report_pagine,report_foto)
        # TODO: valuta report
        return report_pagine

    def evaluate_report(self, report_pagine, report_foto):
        # return report = Report(sito, report_pagine, report_foto,(0,1,2/1,2,3))
        pass
