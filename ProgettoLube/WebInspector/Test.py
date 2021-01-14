import os
import unittest
from os.path import basename
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from bson.objectid import ObjectId
import time
import pymongo
import datetime
import random
from selenium import webdriver

from selenium.webdriver.chrome.options import Options

from Crawler import Crawler
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
        flag_stampa_trend_training = False  # modificare se si vuole vedere il grafico del trend
        ic.create_model(flag_stampa_trend_training)
        start_time = time.time()
        # ic.predict('C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\images\\promo.png')
        # ic.predict('C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\images\\capra.jpg')
        # ic.predict('C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\images\\logo.png')
        # ic.predict('C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\images\\logo2.png')
        # ic.predict('C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\images\\scavolini.png')
        # ic.predict('C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\images\\cane.jpg')
        # ic.predict('C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\images\\car.jpg')
        ic.predict('C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\photo_downloaded\\Lube-Store-Tuscolana-Logo-nero3.png')
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
        url = "https://www.lubebrescia.it/media/widgetkit/cucina-classica-5b0210bc2cc2ff588457b4ce462a3522.jpg"
        # content = urllib.request.urlopen(url, timeout=10)
        path = r"C:\Users\matti\git\ProgettoLube\ProgettoLube\WebInspector\photo_downloaded" + "\\" + \
               basename(
                   'https://www.lubebrescia.it/media/widgetkit/cucina-classica-5b0210bc2cc2ff588457b4ce462a3522.jpg')
        req = Request(
            'https://www.lubebrescia.it/media/widgetkit/cucina-classica-5b0210bc2cc2ff588457b4ce462a3522.jpg',
            headers={'User-Agent': 'Mozilla/5.0'})
        with open(path, "wb") as f:
            content = urlopen(req).read()
            try:
                f.write(content)
            except IOError as e:
                print("I/O error: ".format(e.errno, e.strerror))
        # webpage = urlopen(req).read()
        # print(webpage)
        # soup = BeautifulSoup(browser.page_source, "html.parser")
        # browser.close()
        # for x in soup.find_all('iframe'):
        #     if x.has_attr('src'):
        #         print(x)
        # url = "https://www.lubebrescia.it"
        # options = Options()
        # options.add_argument('--headless')
        # browser = webdriver.Chrome(options=options)
        # browser.get(url)
        # soup = BeautifulSoup(browser.page_source, "html.parser")
        # browser.close()
        # body = soup.find('body')
        # print("BODY :", body)
        # crawler = Crawler()
        # lista = ["https://www.lubebrescia.it/news-cucine/53-ultime-cucine-a-meta-prezzo-brescia.html",
        #          "https://www.lubebrescia.it/#","https://www.lubebrescia.it/news-cucine/54-interiordesign.html"]
        # crawler.scrape_photos("https://www.lubebrescia.it",lista)

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
        range = [1, 3]
        lista1 = db_manager.retrieve_year_average(2020, range)

        for x in lista1:
            print(x)
        # lista2 = db_manager.find_one(6)
        # for x in lista2:
        # print(x)

    def test_time(self):
        # x = datetime.datetime.now().replace(hour=00,minute=00,second=00,microsecond=00)
        print(datetime.datetime(random.randint(2020,2021),random.randint(1,12),random.randint(1,27),
                                 ))

    # print(x)

    def test_excel(self):
        pino = LoadResources()
        dict = pino.load_name_resellers()
        lista = list(dict['INSEGNA/NOME NEGOZIO'].values())
        lista = [x for x in lista if str(x) != 'nan']
        lista = sorted(lista)
        print(lista)
        print(len(lista))

    def test_pandas(self):
        pino = LoadResources()
        pino.load_store_details_name("Lube Creo Store Pratola Peligna")

    def test_path_files(self):
        path = 'dataset_image_ssim\\'
        mypath2 = "C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\"
        paths = [os.path.join(path, fn) for fn in next(os.walk(path))[2]]
        temp = []
        for x in paths:
            temp.append(mypath2 + x)
        print(temp)

    def testttt(self):
        db_manager = DBmanager()
        db_manager.start_connection()
        ciccio = {"name": 'pinoo', "report": 'reportttt'}
        db_manager.insert(ciccio)

    def test_insert(self):
        thisdict2 = {
            "brand": "Ferrari",
            "model": "408",
            "year": 1997
        }
        db = DBmanager()
        db.start_connection()
        load = LoadResources()
        nomi = load.load_name_resellers()
        #range = [1,3]
        lista = []
        for i in range(0, 9, 1):
            for x in nomi:
                date = datetime.datetime(random.randint(2020, 2021), random.randint(1, 12), random.randint(1, 27),
                                         )
                pino = {
                    "date":date,
                    "name":x,
                    "report":thisdict2,
                    "valutazione":random.randint(1,3)
                }
                db.insert(pino)

    def test_scarpe_keyword(self):
        lista = ["https://www.cucineluberoma.it","https://lubecreomilano.it/",]
        crw = Crawler()
        crw.scrape_keyword(lista)

    def test_string(self):
        string = "mystring/"
        if string.endswith('/'):
            string = string[:-1]

        print(string)


if __name__ == '__main__':
    unittest.main()
