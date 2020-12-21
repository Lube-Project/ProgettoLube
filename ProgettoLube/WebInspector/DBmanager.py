#TODO: connessione con vero database forse mongodb e per testing mongocloud
import pymongo

class DBmanager:

    def insert(self, collection, report):
        print(report.toJSON())
        x = collection.insert_one(report.toJSON())

    def delete(self):
        pass

    def update(self):
        pass

    def retrieve_all(self,collection):
        lista = []
        for x in collection.find({}, {"_id": 0, "date": 1, "obj": 1}):
            lista.append(x)
        return lista



