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
        report_foto = img_processor.generate_report_foto('web')
        # report_foto = img_worker.generate_reportfoto()
        # TODO: cancellare directory foto
        report = self.evaluate_report(sito, report_pagine, report_foto)
        # TODO: valuta report
        # report = Report(sito, report_pagine, report_foto, valutazione)
        return report

    def valuta_facebook_profile(self, profilo):
        crawler = CrawlerSocial()
        img_processor = ImageProcessor()
        report = crawler.facebook_crawler(profilo, img_processor)
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

    def evaluate_report(self, sito, report_pagine, report_foto):
        valutazione_script = None
        valutazione_keywords = 1
        valutazione_foto = 1
        si = 0
        ni = 0
        no = 0
        if not report_pagine.dictionary_script:
            valutazione_script = 0
        else:
            valutazione_script = 1
        res = report_pagine.dictionary_parolechiave['resoconto']
        cont = 0
        keywordgood = 0
        keywordni = 0
        keywordno = 0
        for x in res.values():
            if x < 50:
                keywordgood += 1
            if 50 < x < 100:
                keywordni += 1
            if x > 100:
                keywordno += 1
        varmax = {"keywordgood": keywordgood, "keywordni": keywordni, "keywordno": keywordno}
        max_key = max(varmax, key=varmax.get)
        if max_key == "keywordgood":
            valutazione_keywords = 1
        if max_key == "keywordno":
            valutazione_keywords = 3
        if max_key == "keywordni":
            valutazione_keywords = 2
        logo_correctness = report_foto.correttezza_logo['logo_correctness']
        if logo_correctness['lube&creo TUTTO OK'] >= 1 or logo_correctness['lube TUTTO OK'] >= 1 or logo_correctness[
            'creo TUTTO OK'] >= 1:
            si = 1
        if logo_correctness['lube&creo ERRATI'] >= 1 or logo_correctness['lube ERRATI'] >= 1 or logo_correctness[
            'creo ERRATI'] >= 1:
            no = 1
        if logo_correctness['lube&creo loghi ok ma proporzioni o abbinamenti NON CORRETTI'] >= 1 or logo_correctness[
            'lube loghi ok ma proporzioni o abbinamenti NON CORRETTI'] >= 1 or logo_correctness[
            'creo loghi ok ma proporzioni o abbinamenti NON CORRETTI'] >= 1:
            ni = 1

        if si == 0 and no == 0 and ni == 0:
            valutazione_foto = None
        if si == 1 and no == 1 and ni == 1:
            valutazione_foto = 3

        if si == 1 and no == 0 and ni == 0:
            valutazione_foto = 1
        if si == 1 and no == 1 and ni == 0:
            valutazione_foto = 2
        if si == 1 and no == 0 and ni == 1:
            valutazione_foto = 2

        if si == 0 and no == 1 and ni == 0:
            valutazione_foto = 3
        if si == 0 and no == 0 and ni == 1:
            valutazione_foto = 2
        if si == 0 and no == 1 and ni == 1:
            valutazione_foto = 3
        report = Report(sito, report_pagine, report_foto, valutazione_script, valutazione_foto, valutazione_keywords)
        return report
