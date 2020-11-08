import unittest
from Crawler import Crawler
from ImageWorker import ImageWorker


class MyTestCase(unittest.TestCase):

    def test_something(self):
        crawler = Crawler()
        #crawler.test("https://www.caldarolalubestore.com")
        crawler.test2("http://www.caldarolalubestore.com/wp-content/uploads/2020/11/LOGO-CALDAROLA_a_NORMA_2020_250X80.png")
        # TODO:problema con user agent risolvere forse usare altra libreria come urlib,urlib2

    def test_imageworker(self):
        worker = ImageWorker()
        path1 = r"C:\Users\matti\PycharmProjects\WebInspector\images\logo.png"
        path2 = r"C:\Users\matti\PycharmProjects\WebInspector\images\logoc.png"
        worker.processImage(path1, path2)
        #TODO: prima di tutto si deve regolare le due immagini per avere la stessa dimensione


if __name__ == '__main__':
    unittest.main()
