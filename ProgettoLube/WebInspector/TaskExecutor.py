import logging

from DBmanager import DBmanager
from Service import Service


class TaskExecutor:
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger('TaskExecutor')

    db_manager = DBmanager()

    def run_process(self):
        service = Service()
        # Load siti from excel (LoadResources class)
        lista_siti = ["https://www.lubecreostorepratolapeligna.it", ]
        for sito in lista_siti:
            report = service.valuta(sito)
            self.db_manager.insert(report)

        self.logger.info("FINISH")
