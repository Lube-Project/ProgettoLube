import unittest
import urllib
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import time


from ImageClassificator import ImageClassificator
from ImageWorker import ImageWorker
from Report import Report
from ReportFoto import ReportFoto
from ReportPagine import ReportPagine


class MyTestCase(unittest.TestCase):

    def test_imageclassificator(self):
        ic = ImageClassificator()
        flag_stampa_trend_training = False  # modificare se si vuole vedere il grafico del trend
        ic.create_model(flag_stampa_trend_training)
        start_time = time.time()
        ic.predict('C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\images\\promo.png')
        ic.predict('C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\images\\capra.jpg')
        ic.predict('C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\images\\logo.png')
        ic.predict('C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\images\\logo2.png')
        print("TEMPO PREDIZIONI :  %s seconds " % (time.time() - start_time))

    def test_report_structure(self):
        lista = ["pippo", 5, "PAOLO"]
        thisdict = {
            "brand": "Ford",
            "model": "Mustang",
            "year": 1964
        }
        thisdict2 = {
            "brand": "Ferrari",
            "model": "408",
            "year": 1997
        }
        rp = ReportPagine(lista, thisdict, thisdict2)
        thisdict3 = {
            "brand": "Armani",
            "model": "jeans",
            "year": 2000
        }
        thisdict4 = {
            "brand": "The north face",
            "model": "Jacket",
            "year": 2010
        }
        rf = ReportFoto(thisdict3, thisdict4)
        report = Report("sito", rp, rf)
        print(report.toJSON())

    def test_imageworker(self):
        worker = ImageWorker()
        path1 = r"C:\Users\matti\PycharmProjects\WebInspector\images\logo.png"
        path2 = r"C:\Users\matti\PycharmProjects\WebInspector\images\logoc.png"
        worker.processImage(path1, path2)

    def testino(self):
        url = "https://www.lubecreostorepratolapeligna.it/"
        try:
            page = urllib.request.urlopen(url, timeout=20)
        except HTTPError as e:
            page = e.read()
            # soup = BeautifulSoup(page.content, 'html.parser')
        soup = BeautifulSoup(page, 'html.parser')

        print(soup)


if __name__ == '__main__':
    unittest.main()
