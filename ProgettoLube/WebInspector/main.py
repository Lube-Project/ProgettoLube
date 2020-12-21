from TaskExecutor import TaskExecutor
import schedule
import time

executor = TaskExecutor()


def job():
    print("I'm working...")


#schedule.every(2).seconds.do(job)
schedule.every().hour.do(executor.run_process())
# schedule.every().day.at("10:30").do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)



#                                       TENSORFLOW OR OPENCV
# TODO: dato un set di loghi ad una macchina, dargli un immagine e far controllare se l'immagine è un logo
# TODO: se 