import unittest
import urllib
from urllib.error import HTTPError
import re
import json
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

from Crawler import Crawler
from ImageWorker import ImageWorker
from Report import Report
from ReportFoto import ReportFoto
from ReportPagine import ReportPagine


class MyTestCase(unittest.TestCase):

    def test_something(self):
        rp = ReportPagine("ciao", "D", "F")
        rf = ReportFoto("n", "g")
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
