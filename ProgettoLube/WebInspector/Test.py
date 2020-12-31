import os
import unittest
import urllib
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import time
import pymongo

from ImageClassificator import ImageClassificator
from ImageWorker import ImageWorker
from LoadResources import LoadResources
from OpenCV import OpenCV
from DBmanager import DBmanager
from Report import Report
from ReportFoto import ReportFoto
from ReportPagine import ReportPagine


class MyTestCase(unittest.TestCase):

    def test_imageclassificator(self):
        ic = ImageClassificator()
        flag_stampa_trend_training = True  # modificare se si vuole vedere il grafico del trend
        ic.create_model(flag_stampa_trend_training)
        start_time = time.time()
        ic.predict('C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\images\\promo.png')
        ic.predict('C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\images\\capra.jpg')
        ic.predict('C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\images\\logo.png')
        ic.predict('C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\images\\logo2.png')
        ic.predict('C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\images\\scavolini.png')
        ic.predict('C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\images\\cane.jpg')
        ic.predict('C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\images\\car.jpg')
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
        url = "https://www.coop.se/butiker-erbjudanden/coop/coop-ladugardsangen-/"
        try:
            page = urllib.request.urlopen(url, timeout=20)
        except HTTPError as e:
            page = e.read()
        soup = BeautifulSoup(page, 'html.parser')
        lst = ['C', 'B', 'A', 'B']
        lst = list(dict.fromkeys(lst))
        print(lst)

    def test_list_dir(self):
        from os import listdir
        mypath = "photo_downloaded\\"
        mypath2 = "C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector"
        import os
        # files_path = [os.path.abspath(x) for x in os.listdir(mypath)]
        # print(files_path)
        paths = [os.path.join(mypath, fn) for fn in next(os.walk(mypath))[2]]
        temp = []
        for x in paths:
            temp.append(mypath2 + x)
        print(temp)

    def test_OCR(self):
        path = 'C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\images\\logoc.png'
        ocr = OpenCV()
        ocr.read_text_two(path)

    def test_db(self):
        db_manager = DBmanager()
        db_manager.start_connection()
        lista1 = db_manager.retrieve_day_month_year_name(2020, 12, 28, "Pratola Peligna")

        for x in lista1:
            print(x)

    def test_time(self):
        import datetime
        x = datetime.datetime.now()
        x = x.date()
        print(x)

    def test_excel(self):
        pino = LoadResources()
        dict = pino.load_name_resellers()
        lista = list(dict['INSEGNA/NOME NEGOZIO'].values())
        lista = [x for x in lista if str(x) != 'nan']
        lista = sorted(lista)
        print(lista)
        print(len(lista))


if __name__ == '__main__':
    unittest.main()
