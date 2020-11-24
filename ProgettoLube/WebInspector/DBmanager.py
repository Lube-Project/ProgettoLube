#TODO: connessione con vero database forse mongodb e per testing mongocloud
#import pymongo

class DBmanager:

    def insert(self, report):
        print(report.toJSON())
        #myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        #mydb = myclient["webinspector"]
        #mycol = mydb["web_report"]
        #mydict = {"date": "data_report", "obj": "report"}
        #mycol.insert_one(mydict)

    def delete(self):
        pass

    def update(self):
        pass
