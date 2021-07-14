import logging
import os
import urllib
from os.path import basename
from socket import socket
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from instascrape import *
from facebook_scraper import get_posts
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import DashboardConfig
from ReportSocial import ReportSocial


class CrawlerSocial:
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger('CrawlerSocial')

    def facebook_crawler(self, target, img_processor):
        last_post_date = None
        last_month_date = None
        lista_post = []
        for post in get_posts(target, pages=500):
            last_post_date = post['time'] if last_post_date is None else last_post_date
            last_month_date = last_post_date - datetime.timedelta(
                days=DashboardConfig.numeroGiorniToCheckOnSocialProfileActivity) if last_month_date is None else last_month_date
            print("last post date", last_post_date)
            print("last month date", last_month_date)
            print("upload date", post['time'])
            if post['time'] >= last_month_date:
                print('----------------------------------------------------------------------------------')
                print(post)
                lista_post.append(post)
                print('----------------------------------------------------------------------------------')
                time.sleep(5)
            else:
                break
        print("Ho trovato " + str(len(lista_post)) + " posts")
        dictionary_parole_chiave = self.search_keyword_post_fb(lista_post)
        self.download_facebook_photos(lista_post)
        report_foto = img_processor.generate_report_foto('social')
        valutazione_foto = self.evaluate_report_foto_social(report_foto)
        valutazione_keywords = self.evaluate_report_keywords_social(dictionary_parole_chiave)
        report = ReportSocial(social='facebook',
                              quantita_post_neltempo=len(lista_post),
                              dictionary_parolechiave_nel_post=dictionary_parole_chiave,
                              report_foto=report_foto, valutazione_foto=valutazione_foto,
                              valutazione_keywords=valutazione_keywords, nome=target)
        # print(report.toJSON())
        return report

    def download_facebook_photos(self, lista):
        self.logger.info("STARTING PHOTOS DOWNLOAD")
        links = []
        for post in lista:
            links.extend(post['images'])
        for link in links:
            pippo = False
            content = None
            try:
                req = Request(
                    link,
                    headers={'User-Agent': 'Mozilla/5.0'})
                content = urlopen(req).read()
            except (HTTPError, URLError) as error:
                # logging.error('Data of %s not retrieved because %s\nURL: %s', urlimg, error, url)
                pippo = True
            except socket.timeout:
                # logging.error('socket timed out - URL %s', url)
                pippo = True
            except urllib.error.URLError as error:
                # logging.error('Data of %s not retrieved because %s\nURL: %s', urlimg, error, url)
                pippo = True
            a = urlparse(link)
            path = os.path.join(
                r"C:\Users\matti\git\ProgettoLube\ProgettoLube\WebInspector\photo_downloaded" + "\\" + basename(a.path))
            try:
                if not pippo:
                    try:
                        with open(path, "wb") as f:
                            f.write(content)
                    except (OSError, IOError) as e:
                        print("I/O error: ".format(e.errno, e.strerror))
            except IOError as e:
                print("I/O error: ".format(e.errno, e.strerror))
        self.logger.info("FINISH PHOTOS DOWNLOAD")

    def search_keyword_post_fb(self, lista):
        self.logger.info("LOOKING FOR KEYWORDS...")
        urlkeywords = {}
        # key_set = ["sconto", "sconti", "fuori tutto", "promozione", "%", "offerta", "offerte", "promozioni", "€"]
        key_set = DashboardConfig.keywordsCrawlerSocial
        resoconto = {}
        for x in key_set:
            resoconto[x] = 0
        for post in lista:
            temp = []
            for key in key_set:
                # TODO: mettere dopo la parola anche . :
                count = len(re.findall(r'(?<!\S)' + key + r'(?![^!;\r\n\s])', post['post_text'], re.IGNORECASE))
                resoconto[key] = resoconto[key] + count
                self.logger.info(
                    '\nUrl: {}\ncontains {} occurrences of word: {}'.format(post['post_url'], count, key))
                string = 'key ' + key + ' found :' + str(count) + ' times'
                temp.append(string)
            urlmodified = post['post_url'].replace(".", "")
            urlkeywords[urlmodified] = temp
        self.logger.info("FINISH KEYWORD PROCESS")
        Dict = {
            'history': urlkeywords,
            'resoconto': resoconto
        }
        return Dict

    def instagram_crawler(self, target, img_processor):
        last_post_date = None
        last_month_date = None
        s = requests.Session
        # sessionid = '45669560469%3AChazF6EraaLc9A%3A16'
        sessionid = '45669560469%3ASHuSftDoYURSge%3A26'
        lista = []
        # headers = {"User-Agent": "user-agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
        # "cookie": f"sessionid={os.environ.get('sessionid')};"}
        headers = {
            "User-Agent": "user-agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
            "cookie": f"sessionid={sessionid};"}
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options, executable_path='chrome-driver/chromedriver.exe')
        # target = 'https://www.instagram.com/molteni_matteo/'
        # target = 'https://www.instagram.com/lube_marseille_store/'
        insta_profile = Profile(target)
        time.sleep(10)
        insta_profile.scrape(headers=headers)
        time.sleep(10)
        insta_profile.url = target
        driver.get('https://www.instagram.com')
        with open('C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\cookie_instagram.json', 'r',
                  newline='') as input_data:
            cookies = json.load(input_data)
        for i in cookies:
            driver.add_cookie(i)
        list_post = insta_profile.get_posts(webdriver=driver)
        time.sleep(10)
        # print(insta_profile.followers)
        print("Numero post totali : " + str(len(list_post)))
        for profile_post in list_post:
            profile_post.scrape(headers=headers)
            last_post_date = profile_post['upload_date'] if last_post_date is None else last_post_date
            last_month_date = last_post_date - datetime.timedelta(
                days=DashboardConfig.numeroGiorniToCheckOnSocialProfileActivity) if last_month_date is None else last_month_date
            print("last post date", last_post_date)
            print("last month date", last_month_date)
            print("upload date", profile_post['upload_date'])
            if profile_post['upload_date'] >= last_month_date:
                time.sleep(10)
                lst = get_image_urls(profile_post)
                post_dict = profile_post.to_dict(metadata=False)
                post_dict['images_links'] = lst
                lista.append(post_dict)
            else:
                break
        parole_chiave_nelpost = self.search_keyword_post_insta(lista)
        for obj in lista:
            print(obj)
        self.download_insta_photos(lista)
        report_foto = img_processor.generate_report_foto('social')
        valutazione_foto = self.evaluate_report_foto_social(report_foto)
        valutazione_keywords = self.evaluate_report_keywords_social(parole_chiave_nelpost)
        nome = target.replace("https://www.instagram.com/", "")
        report = ReportSocial(social='instagram',
                              quantita_post_neltempo=len(lista),
                              dictionary_parolechiave_nel_post=parole_chiave_nelpost,
                              report_foto=report_foto, valutazione_foto=valutazione_foto,
                              valutazione_keywords=valutazione_keywords, nome=nome.replace("/", ""))
        print(report.toJSON())
        driver.quit()
        print('fine')
        return report

    def search_keyword_post_insta(self, lista_post):
        urlkeywords = {}
        # key_set = ["sconto", "sconti", "fuori tutto", "promozione", "%", "offerta", "offerte", "promozioni", "€"]
        key_set = DashboardConfig.keywordsCrawlerSocial
        resoconto = {}
        for x in key_set:
            resoconto[x] = 0
        for post in lista_post:
            temp = []
            for key in key_set:
                # TODO: mettere dopo la parola anche . :
                count = len(re.findall(r'(?<!\S)' + key + r'(?![^!;\r\n\s])', post['caption'], re.IGNORECASE))
                resoconto[key] = resoconto[key] + count
                self.logger.info(
                    '\nUrl: {}\ncontains {} occurrences of word: {}'.format(post['display_url'], count, key))
                string = 'key ' + key + ' found :' + str(count) + ' times'
                temp.append(string)
            urlmodified = post['display_url'].replace(".", "")
            urlkeywords[urlmodified] = temp
        Dict = {
            'history': urlkeywords,
            'resoconto': resoconto
        }
        return Dict

    def download_insta_photos(self, lista_post):
        links = []
        for post in lista_post:
            links.extend(post['images_links'])
        for link in links:
            pippo = False
            content = None
            try:
                req = Request(
                    link,
                    headers={'User-Agent': 'Mozilla/5.0'})
                content = urlopen(req).read()
            except (HTTPError, URLError) as error:
                # logging.error('Data of %s not retrieved because %s\nURL: %s', urlimg, error, url)
                pippo = True
            except socket.timeout:
                # logging.error('socket timed out - URL %s', url)
                pippo = True
            except urllib.error.URLError as error:
                # logging.error('Data of %s not retrieved because %s\nURL: %s', urlimg, error, url)
                pippo = True
            a = urlparse(link)
            path = os.path.join(
                r"C:\Users\matti\git\ProgettoLube\ProgettoLube\WebInspector\photo_downloaded" + "\\" + basename(a.path))
            try:
                if not pippo:
                    try:
                        with open(path, "wb") as f:
                            f.write(content)
                    except (OSError, IOError) as e:
                        print("I/O error: ".format(e.errno, e.strerror))
            except IOError as e:
                print("I/O error: ".format(e.errno, e.strerror))

    def evaluate_report_foto_social(self, report_foto):
        valutazione_foto = 1
        si = 0
        ni = 0
        no = 0
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
            valutazione_foto = 1
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
        return valutazione_foto

    def evaluate_report_keywords_social(self, dictionary_parole_chiave):
        valutazione_keywords = 1
        res = dictionary_parole_chiave['resoconto']
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
        return valutazione_keywords


def get_image_urls(post):
    """Returns a list of URLs for all images in a scraped Post object"""
    image_urls = {key: val for key, val in post.flat_json_dict.items() if "display_url" in key}
    return list(set(image_urls.values()))
