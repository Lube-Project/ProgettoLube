import unittest

from Crawler import Crawler


class MyTestCase(unittest.TestCase):

    def test_something(self):
        crawler = Crawler()
        #crawler.test("https://www.caldarolalubestore.com")
        crawler.test2("https://www.caldarolalubestore.com/wp-content/uploads/2015/10/Arancini-di-SPINACI.jpg")
        # TODO:problema con user agent risolvere forse usare altra libreria come urlib,urlib2





if __name__ == '__main__':
    unittest.main()
