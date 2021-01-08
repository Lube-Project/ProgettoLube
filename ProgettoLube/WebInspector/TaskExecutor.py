import logging
import schedule
import time
from DBmanager import DBmanager
from Service import Service
import pymongo


class TaskExecutor:
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger('TaskExecutor')

    db_manager = DBmanager()

    client = pymongo.MongoClient(
        "mongodb+srv://molciprom:molciprom@clusterlube.auwyr.mongodb.net/lube_reports?retryWrites=true&w=majority")
    db = client["lube_reports"]
    cl = db["web_reports"]

    def run_process(self):
        service = Service()
        # Load siti from excel (LoadResources class)
        lista_siti = ["https://www.lubecreostorepratolapeligna.it", ]
        #lista_siti = ["https://www.lubebrescia.it", ]
        for sito in lista_siti:
            report = service.valuta(sito)
            # self.db_manager.insert(self.cl,report)

        self.logger.info("FINISH")

# def job():
# print("I'm working...")


# schedule.every(2).seconds.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)

# while 1:
# schedule.run_pending()
# time.sleep(1)
