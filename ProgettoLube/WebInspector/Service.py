from Crawler import Crawler
from CrawlerSocial import CrawlerSocial
from ImageProcessor import ImageProcessor
from ImageWorker import ImageWorker
from Report import Report


class Service:

    def valuta_sito_web(self, sito):
        crawler = Crawler()
        img_processor = ImageProcessor()
        # img_worker = ImageWorker()
        report_pagine = crawler.generate_reportpagine(sito)
        print(report_pagine.toJSON())
        # TODO: generazione report foto
        report_foto = img_processor.run()
        # report_foto = img_worker.generate_reportfoto()
        # TODO: cancellare directory foto
        # report = self.evaluate_report(report_pagine,report_foto)
        # TODO: valuta report
        report = Report(sito, report_pagine, report_foto, None)
        return report

    def valuta_facebook_profile(self, profilo):
        crawler = CrawlerSocial()
        img_processor = ImageProcessor()
        report = crawler.facebook_crawler(profilo,img_processor)
        # TODO: cancellare directory foto
        # TODO: valuta report
        return report

    def valuta_instagram_profile(self, profilo):
        crawler = CrawlerSocial()
        img_processor = ImageProcessor()
        report = crawler.instagram_crawler(profilo, img_processor)
        # TODO: cancellare directory foto
        # TODO: valuta report
        return report

    def evaluate_report(self, report_pagine, report_foto):
        # return report = Report(sito, report_pagine, report_foto,(0,1,2/1,2,3))
        pass
