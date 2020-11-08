import os
import random
import socket
import threading
import time
import urllib.request
import logging
from os.path import basename
from urllib.error import HTTPError, URLError
from socket import timeout

#from fake_useragent import UserAgent

import requests
from bs4 import BeautifulSoup


class Crawler:

    def run(self, index, url):
        logging.basicConfig(
            format='%(asctime)s %(levelname)-8s %(message)s',
            level=logging.INFO,
            datefmt='%Y-%m-%d %H:%M:%S')
        logger = logging.getLogger('Crawler')
        logger.info(
            "-------------------------------------------------------------------------------------------------")
        logger.info("THREAD " + str(index) + " ANALIZZO : " + url)
        logger.info(
            "-------------------------------------------------------------------------------------------------")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
        }
        #page = requests.get(url, headers=headers)
        try:
            page = urllib.request.urlopen(url, timeout=20)
        except HTTPError as e:
            page = e.read()
        #soup = BeautifulSoup(page.content, 'html.parser')
        soup = BeautifulSoup(page, 'html.parser')
        body = soup.find('body')
        images = body.findAll('img')
        for image in images:
            # counter = counter + 1
            urlimg = image['src']
            if urlimg[0:2] == "//":
                urlimg = urlimg.lstrip('/')
            if urlimg[0:4] != "http" and urlimg[0:3] != "www":
                urlimg = self + urlimg
            if urlimg[0:3] == "www":
                urlimg = "http://" + urlimg
            urlimg = Crawler.eliminaParametriImgUrl(urlimg)
            path = os.path.join(
                r"C:\Users\matti\PycharmProjects\WebInspector\images" + "\\" + basename(
                    urlimg))
            logger.info("THREAD " + str(index) + " SALVO " + urlimg)
            # logger.info(path)
            if urlimg != "":
                # imgsize = requests.get(urlimg, headers=headers).content
                imgsize = 10
                size = 0  # FILTRO modifica per regolare la grandezza desiderata dell'immagine da scaricare es:10*1024=10k
                if imgsize > size:
                    with open(path, "wb") as f:
                        try:
                            content = urllib.request.urlopen(urlimg, timeout=10).read()
                        except (HTTPError, URLError) as error:
                            logging.error('Data of %s not retrieved because %s\nURL: %s', urlimg, error, url)
                        except socket.timeout:
                            logging.error('socket timed out - URL %s', urlimg)
                        except urllib.error.URLError as error:
                            logging.error('Data of %s not retrieved because %s\nURL: %s', urlimg, error, url)
                        try:
                            f.write(content)
                        except IOError as e:
                            print("I/O error: ".format(e.errno, e.strerror))

    # Per trovare tutti i sotto link di un sito root da cui scaricare le foto
    # forse bisognerebbe riusarlo anche per i sotto link stessi
    # Ritorna la lista dei sotto link di un seed
    def start(self, lista):
        logging.basicConfig(
            format='%(asctime)s %(levelname)-8s %(message)s',
            level=logging.INFO,
            datefmt='%Y-%m-%d %H:%M:%S')
        logger = logging.getLogger('Crawler')
        for element in lista:
            logger.info("START CRAWLING SEED : " + element)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
            }
            #page = requests.get(element, headers=headers)
            try:
                page = urllib.request.urlopen(element, timeout=20)
            except HTTPError as e:
                page = e.read()
            #soup = BeautifulSoup(page.content, 'html.parser')
            soup = BeautifulSoup(page, 'html.parser')
            lista = []
            for a in soup.find_all('a', href=True):
                href = ''
                if a['href'][0:4] != 'http':
                    if a['href'][0:1] != "/":
                        href = element + "/" + a['href']
                    if a['href'][0:1] == "/":
                        href = element + a['href']
                    lista.append(href)
                if a['href'][0:4] == 'http':
                    lista.append(a['href'])
            cleaned = [x for x in lista if element in x]
            cleaned = list(dict.fromkeys(cleaned))
            threads = [threading.Thread(target=Crawler.run, args=(element, cleaned.index(url), url,))
                       for url in cleaned]
            for t in threads:
                t.start()
            time.sleep(40)

    # Per pulire i parametri dagli url delle immagini
    def eliminaParametriImgUrl(self):
        stripped = ''
        if ".jpg" in self:
            stripped = self.split(".jpg", 1)[0] + ".jpg"
        if ".bmp" in self:
            stripped = self.split(".bmp", 1)[0] + ".bmp"
        if ".gif" in self:
            stripped = self.split(".gif", 1)[0] + ".gif"
        if ".jpeg" in self:
            stripped = self.split(".jpeg", 1)[0] + ".jpeg"
        if ".png" in self:
            stripped = self.split(".png", 1)[0] + ".png"
        if ".tiff" in self:
            stripped = self.split(".tiff", 1)[0] + ".tiff"
        return stripped

    def test2(self, link):
        #ua = UserAgent();
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36'}
        path = os.path.join(
            r"C:\Users\matti\PycharmProjects\WebInspector\images" + "\\" + basename(
                link))
        with open(path, "wb") as f:
            try:
                #content = requests.get(link, headers).content
                content = urllib.request.urlopen(link).read()
            except requests.exceptions.ConnectionError:
                requests.status_codes = "Connection refused"
            try:
                print(content)
                print("SCRIVO  ")
                f.write(content)
            except IOError as e:
                print("I/O error: ".format(e.errno, e.strerror))

    def test(self, seed):
        headers = {'user-agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
        page = requests.get(seed, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        body = soup.find('body')
        lista = []
        for a in soup.find_all('a', href=True):
            href = ''
            if a['href'][0:4] != 'http':
                if a['href'][0:1] != "/":
                    href = seed + "/" + a['href']
                if a['href'][0:1] == "/":
                    href = seed + a['href']
                lista.append(href)
            if a['href'][0:4] == 'http':
                lista.append(a['href'])
        cleaned = [x for x in lista if seed in x]
        cleaned = list(dict.fromkeys(cleaned))
        for element in cleaned:
            print(element)
        print("-----------------------------------------------------------------------------------")
        images = body.findAll('img')
        for image in images:
            # counter = counter + 1
            urlimg = image['src']
            if urlimg[0:2] == "//":
                urlimg = urlimg.lstrip('/')
            if urlimg[0:4] != "http" and urlimg[0:3] != "www":
                urlimg = seed + urlimg
            urlimg = Crawler.eliminaParametriImgUrl(urlimg)
            print(urlimg)


