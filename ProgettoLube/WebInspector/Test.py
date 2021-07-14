import datetime
import os
import random
import time
import unittest
import urllib
from urllib.parse import urlparse
from os.path import basename
from socket import socket
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options

import DashboardConfig
from Crawler import Crawler
from CrawlerSocial import CrawlerSocial
from DBmanager import DBmanager
from ImageClassificator import ImageClassificator
from ImageProcessor import ImageProcessor
from ImageWorker import ImageWorker
from LoadResources import LoadResources
from OpenCV import OpenCV
from Report import Report
from ReportFoto import ReportFoto
from ReportPagine import ReportPagine
from instascrape import *
from facebook_scraper import get_posts

from ReportSocial import ReportSocial


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
        ic.predict(
            'C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\photo_downloaded\\Lube-Store-Tuscolana-Logo-nero3.png')
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
        path = r'C:\Users\matti\OneDrive\Immagini\logopp.png'
        ocr = OpenCV()
        ocr.read_text_two(path)

    def test_db(self):
        db_manager = DBmanager()
        db_manager.start_connection()
        range = [1, 3]
        lista1 = db_manager.retrieve_last()

        for x in lista1:
            print(x)
        # lista2 = db_manager.find_one(6)
        # for x in lista2:
        # print(x)

    def test_time(self):
        # x = datetime.datetime.now().replace(hour=00,minute=00,second=00,microsecond=00)
        oggi = datetime.date.today()
        trentaggfa = oggi - datetime.timedelta(days=30)
        # lastMonth = today - datetime.timedelta(days=1)
        print(trentaggfa)

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
        with open(
                "C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\test_results\\instagram\\lube-creo-store-napoli.json") as f:
            data = json.load(f)
        report = data
        # date = datetime.datetime.now()
        # report['date'] = date
        db_manager.insert_instagram_report(report)

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
        # range = [1,3]
        lista = []
        for i in range(0, 9, 1):
            for x in nomi:
                date = datetime.datetime(random.randint(2020, 2021), random.randint(1, 12), random.randint(1, 27),
                                         )
                pino = {
                    "date": date,
                    "name": x,
                    "report": thisdict2,
                    "valutazione": random.randint(1, 3)
                }
                db.insert(pino)

    def test_scarpe_keyword(self):
        lista = ["https://www.cucineluberoma.it", "https://lubecreomilano.it/", ]
        crw = Crawler()
        crw.scrape_keyword(lista)

    def test_string(self):
        options = Options()
        options.add_argument('--headless')
        browser = webdriver.Chrome(options=options)
        page = None
        try:
            browser.get("https://www.cucinelubenapoli.it/cucine-lube")
            page = browser.page_source
        except WebDriverException as e:
            print("Selenium Exception: {0} Message: {1}".format("my message", str(e)))
        soup = BeautifulSoup(page, "html.parser")
        browser.close()
        browser.quit()
        body = soup.find('body')
        images = body.findAll('img')
        for image in images:
            if image.has_attr('src') or image.has_attr('data-src'):
                print(image['src']) if image.has_attr('src') else print(image['data-src'])

    def test_facebook_scraper(self):
        # TIME: 36m 49s Pratola Peligna 2007 post trovati
        db = DBmanager()
        db.start_connection()
        # target = 'pro.muccia'  # 'ProLocoSerravallediChientiMC'  # 'pro.muccia' 'ProLocoSerravallediChientiMC'
        target = 'LubeCreoNapoli'#'CucineLubecreokitchenspratolapeligna'
        proc = ImageProcessor()
        crawler = CrawlerSocial()
        report = crawler.facebook_crawler(target, proc)
        print(report.toJSON())

    def test_instgram_scraper(self):
        db = DBmanager()
        db.start_connection()
        proc = ImageProcessor()
        socialCrawl = CrawlerSocial()
        # target = 'https://www.instagram.com/lube_marseille_store/'
        # target = 'https://www.instagram.com/molteni_matteo/'
        target = 'https://www.instagram.com/cucinelubenapoli/'
        report = socialCrawl.instagram_crawler(target, proc)
        print(report.toJSON())

    def test_json(self):
        # response = requests.get('https://api.github.com/').json()
        date = datetime.datetime.now()
        print(date)

    def testroba(self):
        from selenium import webdriver

        # sessionid = '45669560469%3AChazF6EraaLc9A%3A16'
        # cookie = {"name": "sessionid", "value": f"{sessionid};", "domain": "www.instagram.com"}
        driver = webdriver.Chrome()
        driver.get('https://www.instagram.com')
        with open('C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\cookie_instagram.json', 'r',
                  newline='') as input_data:
            cookies = json.load(input_data)
        for i in cookies:
            driver.add_cookie(i)
        driver.get('https://www.instagram.com')

    def test_basename(self):
        url = 'https://scontent-fco1-1.cdninstagram.com/v/t51.2885-15/e35/122934023_1083903042041257_2189170774886622649_n.jpg?_nc_ht=scontent-fco1-1.cdninstagram.com&_nc_cat=101&_nc_ohc=ZPwJuG5Ru2AAX89RtbU&tp=1&oh=e83c58cddac8997b4e30364c04c78266&oe=603DE74D'
        a = urlparse(url)
        print(os.path.basename(a.path))

    def test_crawler_run(self):
        crawler = Crawler()
        crawler.run("https://www.cucinelubenapoli.it/", 0, "https://www.cucinelubenapoli.it/")

    def test_image_processor(self):
        proc = ImageProcessor()
        result = proc.run()
        print(result)

    def test_download(self):
        crawler = Crawler()
        with open(r'C:\Users\matti\OneDrive\Desktop\lista.txt') as f:
            content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        content = [x.strip() for x in content]
        for x in content:
            print(x)
        crawler.scrape_photos("https://www.cucineluberoma.it/", content)

    def test_db_keywords(self):
        db = DBmanager()
        db.start_connection()
        lista = db.retrieve_keywords()
        for x in lista:
            print(x)

    def test_config(self):
        # lista = DashboardConfig.keywords
        c = {'pippo': 1}
        d = {'x': 2, 'y': 3}
        paolo = {
            'c': c,
            'resoconto': d
        }
        # print(paolo)
        res = paolo['resoconto']
        cont = 0
        for x in res.values():
            cont = cont + x
        fin = cont / len(res.values())
        print(fin)

    def test_for(self):
        db = DBmanager()
        db.start_connection()
        lista = []
        for z in db.collection_facebook.aggregate([
            {'$sort': {
                'date': 1
            }},
            {'$group': {
                "_id": "$nome",
                'id': {'$last': '$_id'},
                "nome": {'$last': '$nome'},
                'date': {'$last': '$date'},
                "social": {'$last': '$social'},
                "report_foto": {'$last': '$report_foto'},
                "dictionary_parolechiave_nel_post": {'$last': '$dictionary_parolechiave_nel_post'},
                "quantita_post_neltempo": {'$last': '$quantita_post_neltempo'},
                "valutazione_foto": {'$last': '$valutazione_foto'},
                "valutazione_keywords": {'$last': '$valutazione_keywords'}
            }}

        ]):
            lista.append(z)
        for x in lista:
            print(x)

    def test_stupido(self):
        stringa = '//lubecreostorefabriano.com/wp-content/uploads/revslider/homepage_2019/LUBE.png'
        if stringa[0:2] == "//":
            # urlimg = urlimg.lstrip('/')
            print(1)
        elif stringa[0:1] == "/":
            print(2)


def get_image_urls(post):
    """Returns a list of URLs for all images in a scraped Post object"""
    image_urls = {key: val for key, val in post.flat_json_dict.items() if "display_url" in key}
    return list(set(image_urls.values()))


if __name__ == '__main__':
    unittest.main()
