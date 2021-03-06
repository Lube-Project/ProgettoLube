import os
import re

import socket
import threading
import time
import urllib.request
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import logging
from os.path import basename
from urllib.error import HTTPError, URLError

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium import webdriver

from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

import DashboardConfig
from ReportPagine import ReportPagine


class Crawler:
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger('Crawler')

    def run(self, root, index, url):

        self.logger.info(
            "-------------------------------------------------------------------------------------------------")
        self.logger.info("THREAD " + str(index) + " ANALIZZO : " + url)
        self.logger.info(
            "-------------------------------------------------------------------------------------------------")
        options = Options()
        options.add_argument('--headless')
        page = None
        soup = None
        try:
            browser = webdriver.Chrome(options=options, executable_path='chrome-driver/chromedriver.exe')
            browser.get(url)
            page = browser.page_source
        except WebDriverException as e:
            print("Selenium Exception: {0} Message: {1}".format("my message", str(e)))
        if page is not None:
            soup = BeautifulSoup(page, "html.parser")
            if soup is not None:
                browser.close()
                browser.quit()
                body = soup.find('body')
                if body:
                    images = body.findAll('img')
                    # TODO: data-src ci puo essere nell'img oltre src
                    for image in images:
                        # counter = counter + 1
                        if image.has_attr('src') or image.has_attr('data-src'):
                            urlimg = image['src'] if image.has_attr('src') else image['data-src']
                            #self.logger.info("URLIMG TROVATO : " + urlimg)
                            #TODO: fare l'if se url inizia con un solo slash ovverro aggiunger root
                            if urlimg[0:2] == "//":
                               # urlimg = urlimg.lstrip('/')
                                 urlimg = "https:"+urlimg
                            elif urlimg[0:1] == "/":
                                radice = root[:-1]
                                urlimg = radice+urlimg
                            if urlimg[0:4] != "http" and urlimg[0:3] != "www" and urlimg[0:4] != "https":
                                urlimg = root + urlimg
                            if urlimg[0:3] == "www":
                                urlimg = "http://" + urlimg
                            #self.logger.info("URLIMG PULITO : " + urlimg)
                            # urlimg = self.elimina_parametri_url_img(urlimg) #TODO:ATTENTION
                            a = urlparse(urlimg)
                            path = os.path.join(
                                r"C:\Users\matti\git\ProgettoLube\ProgettoLube\WebInspector\photo_downloaded" + "\\" + basename(
                                    a.path))
                            self.logger.info("THREAD " + str(index) + " SALVO " + urlimg)
                            # logger.info(path)
                            if urlimg != "":
                                # imgsize = requests.get(urlimg, headers=headers).content
                                imgsize = 10
                                size = 0  # FILTRO modifica per regolare la grandezza desiderata dell'immagine da scaricare
                                # es:10*1024=10k
                                if imgsize > size:
                                    content = None
                                    pippo = False
                                    try:
                                        req = Request(
                                            urlimg,
                                            headers={'User-Agent': 'Mozilla/5.0'})
                                        content = urlopen(req).read()
                                    except (HTTPError, URLError) as error:
                                        logging.error('Data of %s not retrieved because %s\nURL: %s', urlimg, error,
                                                      url)
                                        if error.code == 406:
                                            try:
                                                self.logger.info("RIPROVO CON UN ALTRO HEADER")
                                                req = Request(
                                                    urlimg,
                                                    headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
                                                content = urlopen(req).read()
                                            except (HTTPError, URLError) as error:
                                                logging.error('Data of %s not retrieved because %s\nURL: %s', urlimg,
                                                              error,
                                                              url)
                                                pippo = True
                                    except socket.timeout:
                                        logging.error('socket timed out - URL %s', urlimg)
                                        pippo = True
                                    except urllib.error.URLError as error:
                                        logging.error('Data of %s not retrieved because %s\nURL: %s', urlimg, error,
                                                      url)
                                        pippo = True
                                    try:
                                        if not pippo:
                                            try:
                                                with open(path, "wb") as f:
                                                    try:
                                                        f.write(content)
                                                        self.logger.info(
                                                            "THREAD " + str(index) + " HO SALVATO " + urlimg)
                                                    except IOError as e:
                                                        self.logger.error('1')
                                                        self.logger.error(e.errno)
                                                        self.logger.error(e)
                                                        self.logger.error(path)
                                                        self.logger.error("I/O error: ".format(e.errno, e.strerror))
                                                        self.logger.error(content)
                                                    except TypeError as t:
                                                        self.logger.error("error")
                                            except (OSError, IOError) as e:
                                                self.logger.error('2')
                                                self.logger.error(e.errno)
                                                self.logger.error(e)
                                                self.logger.error(path)
                                                self.logger.error("I/O error: ".format(e.errno, e.strerror))
                                                self.logger.error(content)
                                    except IOError as e:
                                        self.logger.error('3')
                                        self.logger.error(e.errno)
                                        self.logger.error(e)
                                        self.logger.error(path)
                                        self.logger.error("I/O error: ".format(e.errno, e.strerror))
                                        self.logger.error(content)
        self.logger.info("THREAD " + str(index) + " HO FINITO LE FOTO DA SCARICARE")

    # Per pulire i parametri dagli url delle immagini
    def elimina_parametri_url_img(self, url):
        stripped = ''
        if ".jpg" in url:
            stripped = url.split(".jpg", 1)[0] + ".jpg"
        if ".bmp" in url:
            stripped = url.split(".bmp", 1)[0] + ".bmp"
        if ".gif" in url:
            stripped = url.split(".gif", 1)[0] + ".gif"
        if ".jpeg" in url:
            stripped = url.split(".jpeg", 1)[0] + ".jpeg"
        if ".png" in url:
            stripped = url.split(".png", 1)[0] + ".png"
        if ".tiff" in url:
            stripped = url.split(".tiff", 1)[0] + ".tiff"
        return stripped

    def find_href(self, root, child, ref):
        options = Options()
        options.add_argument('--headless')
        # options.add_argument("start-maximized")
        page = None
        soup = None
        cleaned = []
        try:
            browser = webdriver.Chrome(chrome_options=options, executable_path='chrome-driver/chromedriver.exe')
            browser.get(child)
            page = browser.page_source
        except WebDriverException as e:
            print("Selenium Exception: {0} Message: {1}".format("my message", str(e)))
        if page is not None:
            soup = BeautifulSoup(page, "html.parser")
            if soup is not None:
                browser.close()
                # browser.quit()
                lista = []
                links = []
                esclusioni = ['.jpg', '.bmp', '.gif', '.jpeg', '.png', '.tiff', '.cssjs', '.mid', '.mp2', '.mp3',
                              '.mp4',
                              '.wav',
                              '.avi', '.mov', '.mpeg', '.ram', '.m4v', '.pdf', '.rm', '.smil', '.wmv', '.swf', '.wma',
                              '.zip',
                              '.rar', '.gz', '/tel:', '/mailto:', 'javascript', '.js', 'http://pinterest.com/'
                    , 'https://pinterest.com/', 'http://twitter.com/', 'https://twitter.com/',
                              'https://www.facebook.com/',
                              'http://www.facebook.com/', 'https://plus.google.com/', 'http://plus.google.com/',
                              'https://www.linkedin.com/', 'http://www.linkedin.com/']
                for a in soup.find_all('a', href=True):
                    # print(a)
                    href = ''
                    if a['href'][0:4] != 'http':
                        if a['href'][0:1] != "/":
                            href = root + "/" + a['href']
                        if a['href'][0:1] == "/":
                            href = root + a['href']
                        lista.append(href)
                    if a['href'][0:4] == 'http':
                        lista.append(a['href'])
                cleaned = [x for x in lista if root in x]
                # print(len(cleaned))
                cleaned = list(dict.fromkeys(cleaned))
                cleaned = [s for s in cleaned if not any(xs in s for xs in esclusioni)]
                # str = 'lube'
                no = 'www.cucinelube.it/'
                # seguo solo gli iframe che contengono la parola lube o la root del sito ma se l'iframe è della lube no
                iframelube = []
                for x in soup.find_all('iframe'):
                    if x.has_attr('src'):
                        if no not in x['src']:
                            if x['src'].startswith(root):
                                print("IFRAME : ", x['src'])
                                iframelube.append(x['src'])
                soup.decompose()
                if len(iframelube) > 0:
                    for x in iframelube:
                        try:
                            req = Request(
                                x,
                                headers={'User-Agent': 'Mozilla/5.0'})
                            page = urlopen(req)
                        except HTTPError as e:
                            page = e.read()
                        frame = BeautifulSoup(page, 'html.parser')
                        for a in frame.find_all('a', href=True):
                            href = ''
                            if a['href'][0:4] != 'http':
                                if a['href'][0:1] != "/":
                                    href = root + "/" + a['href']
                                if a['href'][0:1] == "/":
                                    href = root + a['href']
                                cleaned.append(href)
                            if a['href'][0:4] == 'http':
                                cleaned.append(a['href'])
                        frame.decompose()
                cleaned = [x for x in cleaned if root in x]
                cleaned = list(dict.fromkeys(cleaned))
                for x in ref:
                    if x in cleaned:
                        cleaned.remove(x)
                cleaned = [s for s in cleaned if not any(xs in s for xs in esclusioni)]
                browser.quit()
        return cleaned

    def generate_reportpagine(self, sito):
        self.logger.info("START REPORT : " + sito)
        # FIND HREF LIST
        lista_href = self.scrape_href(sito)
        # FOR EACH HREF : SCARICA FOTO, CERCA SCRIPT, CERCA KEYWORD
        flag = self.scrape_photos(sito, lista_href)
        dict_script = self.scrape_script(lista_href)
        dict_keyword = self.scrape_keyword(lista_href)
        report_pagine = ReportPagine(lista_href, dict_script, dict_keyword)
        # self.logger.info("FINISH REPORT PAG : " + sito)
        return report_pagine

    def scrape_href(self, sito):
        if sito.endswith('/'):
            sito = sito[:-1]
        lista = [sito]
        count = 0
        for e in lista:
            ref = lista
            count = count + 1
            self.logger.info("VALUTO LINK : " + e + " N. " + str(count))
            # se tutti i link che torna il findhref sono dentro lista skippa l'append
            temp = self.find_href(sito, e, ref)
            for x in temp:
                self.logger.info("ADD TO TAIL :" + x)
            for element in temp:
                if element in lista:
                    temp.remove(element)
            lista.extend(temp)
            self.logger.info("La lunghezza della lista è : " + str(len(lista)))
        lista = [x for x in lista if sito in x]
        lista = list(dict.fromkeys(lista))
        for x in lista:
            self.logger.info("FINAL :" + x)
        self.logger.info("FINAL LENGTH : " + str(len(lista)))
        return lista

    def scrape_photos(self, sito, lista_href):
        flag = True
        # threads = [threading.Thread(target=self.run, args=(sito, lista_href.index(url), url,))
        #            for url in lista_href]
        # for t in threads:
        #     t.start()
        for x in lista_href:
            self.logger.info("inizio sub processo download")
            self.run(sito, lista_href.index(x), x)
            self.logger.info("fine sub processo download")
        return flag

    def scrape_script(self, lista_href):
        self.logger.info("SCRAPING SCRIPT...")
        Dict = {}
        page = None
        soup = None
        key = 'api.gruppolube.it'
        for url in lista_href:
            try:
                req = Request(
                    url,
                    headers={'User-Agent': 'Mozilla/5.0'})
                page = urlopen(req)
            except HTTPError as e:
                page = e.read()
            if page is not None:
                soup = BeautifulSoup(page, 'html.parser')
                if soup is not None:
                    for script in soup.find_all('script', {"src": True}):
                        if key in script['src']:
                            self.logger.info("FOUND SCRIPT : " + script['src'] + " IN " + url)
                            urlmodified = url.replace(".", "")
                            Dict[urlmodified] = script['src']
        return Dict

    def scrape_keyword(self, lista_href):
        self.logger.info("LOOKING FOR KEYWORDS...")
        urlkeywords = {}
        page = None
        soup = None
        # key_set = ["sconto", "sconti", "fuori tutto", "promozione", "%", "offerta", "offerte", "promozioni", "€"]
        key_set = DashboardConfig.keywordsCrawler
        resoconto = {}
        for x in key_set:
            resoconto[x] = 0
        for url in lista_href:
            temp = []
            try:
                req = Request(
                    url,
                    headers={'User-Agent': 'Mozilla/5.0'})
                page = urlopen(req)
            except HTTPError as e:
                page = e.read()
            if page is not None:
                soup = BeautifulSoup(page, 'html.parser')
                if soup is not None:
                    body = soup.find('body')
                    if body:
                        text = body.prettify()
                        for key in key_set:
                            # TODO: mettere dopo la parola anche . :
                            count = len(re.findall(r'(?<!\S)' + key + r'(?![^!;\r\n\s])', text, re.IGNORECASE))
                            resoconto[key] = resoconto[key] + count
                            self.logger.info('\nUrl: {}\ncontains {} occurrences of word: {}'.format(url, count, key))
                            string = 'key ' + key + ' found :' + str(count) + ' times'
                            temp.append(string)
                        urlmodified = url.replace(".", "")
                        urlkeywords[urlmodified] = temp
        Dict = {
            'history': urlkeywords,
            'resoconto': resoconto
        }
        return Dict
