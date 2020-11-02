import os
import urllib
import logging
from os.path import basename

import requests
from bs4 import BeautifulSoup


class Crawler:

    url = ''

    def __init__(self, url):
        # Instance Variable
        self.url = url

    # TODO: controllare anche i tag picture o altri(boh) perche le immagini non stanno solo dentro i tag img
    def avvia(self):
        logging.basicConfig(
            format='%(asctime)s %(levelname)-8s %(message)s',
            level=logging.INFO,
            datefmt='%Y-%m-%d %H:%M:%S')
        logger = logging.getLogger('Crawler')
        lista = Crawler.findhref(self, self.url)
        counter = 0
        for element in lista:
            logger.info(
                "-------------------------------------------------------------------------------------------------")
            logger.info("ANALIZZO : " + element)
            logger.info(
                "-------------------------------------------------------------------------------------------------")
            page = requests.get(element)
            soup = BeautifulSoup(page.content, 'html.parser')
            body = soup.find('body')
            images = body.findAll('img')
            for image in images:
                # counter = counter + 1
                urlimg = image['src']
                if urlimg[0:4] != "http":
                    urlimg = self.url + urlimg
                urlimg = Crawler.eliminaParametriImgUrl(self, urlimg)
                logger.info("Salvo immagine")
                path = os.path.join(
                    r"C:\Users\matti\git\ProgettoLube\ProgettoLube\WebInspector\images" + "\\" + basename(
                        urlimg))
                logger.info(urlimg)
                logger.info(path)
                # TODO: fare un if dove si controlla requests.get(urlimg).content se restituisce qualcosa che è minore di 10k
                if urlimg != "":
                    imgsize = requests.get(urlimg).content
                    size = 0  # FILTRO modifica per regolare la grandezza desiderata dell'immagine da scaricare es:10*1024=10k
                    if len(imgsize) > size:
                        with open(path, "wb") as f:
                            f.write(requests.get(urlimg).content)

    # Per trovare tutti i sotto link di un sito root da cui scaricare le foto
    # forse bisognerebbe riusarlo anche per i sotto link stessi
    # Ritorna la lista dei sotto link di un seed
    def findhref(self, root):
        page = requests.get(root)
        soup = BeautifulSoup(page.content, 'html.parser')
        lista = [root]
        for a in soup.find_all('a', href=True):
            if a['href'][0:4] != 'http':
                if a['href'][0:1] != "/":
                    href = root + "/" + a['href']
                if a['href'][0:1] == "/":
                    href = root + a['href']
                lista.append(href)
            if a['href'][0:4] == 'http':
                lista.append(a['href'])
        cleaned = [x for x in lista if root in x]
        return cleaned

    # Per pulire i parametri dagli url delle immagini
    def eliminaParametriImgUrl(self, src):
        stripped = ''
        if ".jpg" in src:
            stripped = src.split(".jpg", 1)[0] + ".jpg"
        if ".bmp" in src:
            stripped = src.split(".bmp", 1)[0] + ".bmp"
        if ".gif" in src:
            stripped = src.split(".gif", 1)[0] + ".gif"
        if ".jpeg" in src:
            stripped = src.split(".jpeg", 1)[0] + ".jpeg"
        if ".png" in src:
            stripped = src.split(".png", 1)[0] + ".png"
        if ".tiff" in src:
            stripped = src.split(".tiff", 1)[0] + ".tiff"
        return stripped

    def test(self, src):
        page = requests.get(src)
        soup = BeautifulSoup(page.content, 'html.parser')
        body = soup.find('body')
        images = body.findAll('img')
        for img in images:
            print(img)
        for a in soup.find_all('a', href=True):
            print(a['href'])



