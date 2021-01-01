# TODO: RICORDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA che il nome in input ai metodi va controllato lato frontend dandogli al medesimo la tabella excel
# TODO:FARE menu a tendina dove mostri tutti i nomi dei siti, così non bisogna controllare la validità del nome
# TODO: RICORDAAA DI CONTROLLARE IL RANGE DELLA VALUTAZIONE LATO FRONTEND: !=0 AND <4

import pymongo
import datetime


class DBmanager:
    client = None
    db = None
    collection = None

    def start_connection(self):
        self.client = pymongo.MongoClient(
            "mongodb+srv://molciprom:molciprom@clusterlube.auwyr.mongodb.net/lube_reports?retryWrites=true&w=majority")
        self.db = self.client["lube_reports"]
        self.collection = self.db["web_reports"]

    def insert(self, collection, report):
        print(report.toJSON())
        x = collection.insert_one(report.toJSON())

    def delete(self):
        pass

    def update(self):
        pass

    def retrieve_all(self, collection, name):
        lista = []
        for x in collection.find({"name": name}, {"_id": 0, "date": 1, "report": 1, "name": 1, "valutazione": 1}):
            lista.append(x)
        return lista

    # return last document
    def retrieve_last(self):
        sup = []
        lista = []
        date = []
        for x in self.collection.find({}).sort([("date", -1)]).limit(1):
            sup.append(x)
        date = x['date']
        # for x in self.collection.find({"date": date}, {"_id": 0, "date": 1, "report": 1, "name": 1, "valutazione": 1}):
        # lista.append(x)
        for z in self.collection.aggregate([
            {
                "$project": {
                    "_id": 0,
                    "id":"$_id",
                    "date": 1,
                    "report": 1,
                    "name": 1,
                    "valutazione": 1
                }
            },
            {"$match": {"date": date}},
        ]):
            lista.append(z)
        return lista

    ######################### DETTAGLI SITO ###########################################
    # return year(x) documents
    def retrieve_year(self, collection, year):
        # TODO: fare report medio su 365 usando il campo valutazione o se si riesce anche gli altri campi e tornare anche tutti i relativi report
        pass

    # return month(x) of the year(x) documents
    def retrieve_month(self, collection, month, year):
        # TODO: fare report medio su numero report usando il campo valutazione o se si riesce anche gli altri campi e tornare anche tutti i relativi report
        pass

    # return day-month-year(x) documents
    def retrieve_dayMonthYear(self, collection, year, month, day):
        # TODO: stuff
        pass

    ################################## HOME #################################################

    # return year(x) average reports
    def retrieve_year_average(self, year, range):
        # TODO: ritornare tutti i report medi dell'anno x ogni sito
        # Attualmente: Nel db ho inserito tutte macchine, la media è sull'anno all'interno dell'oggetto obj
        lista = []
        for z in self.collection.aggregate([
            {
                "$project": {
                    "year": {"$year": "$date"},
                    "name": 1,
                    "average": "$valutazione",
                }
            },
            {"$match": {"year": year}},
            {
                "$group": {
                    "_id": "$name",
                    "valutazione": {"$avg": "$average"},
                    "year": {"$first": year},
                }
            }, {"$addFields": {
                "valutazione": {"$trunc": ["$valutazione", 2]},
            }},
            {"$match": {"valutazione": {"$gte": range[0], "$lte": range[1]}}}
        ]):
            lista.append(z)
        return lista

    # return month(x) of the year(x) average reports
    def retrieve_month_year_average(self, year, month, range):
        # TODO: ritornare tutti i report medi del mese x dell'anno x per ogni sito
        # Ci sono due match perchè se il controllo del range sarebbe stato nel primo, nel calcolo della media avrebbe escluso i campi fuori dal range
        # In questo modo, invece, escludo la valutazione media
        lista = []
        for z in self.collection.aggregate([
            {
                "$project": {
                    "year": {"$year": "$date"},
                    "month": {"$month": "$date"},
                    "name": 1,
                    "average": "$valutazione",
                }
            },
            {"$match": {"year": year, "month": month}},
            {
                "$group": {
                    "_id": "$name",
                    "valutazione": {"$avg": "$average"},
                    "year": {"$first": year},
                    "month": {"$first": month}
                }
            }, {"$addFields": {
                "valutazione": {"$trunc": ["$valutazione", 2]},
            }},
            {"$match": {"valutazione": {"$gte": range[0], "$lte": range[1]}}}
        ]):
            lista.append(z)
        return lista

    # return day(x) of month(x) of the year(x) average reports
    def retrieve_day_month_year(self, year, month, day, range):
        # TODO: ritornare tutti i report del giorno x del mese x dell'anno x per ogni sito
        lista = []
        for z in self.collection.aggregate([
            {
                "$project": {
                    "year": {"$year": "$date"},
                    "month": {"$month": "$date"},
                    "day": {"$dayOfMonth": "$date"},
                    "name": 1,
                    # "valutazione": {"$cond": {"if": { "$and": [{"$ne": [range[0], 0]}, {"$ne": [range[1], 0]}, {"$lt": [range[0], 4]},{"$lt": [range[1], 4]}]},"then": {"$cond": {"if": {"$and": [{"$gte": ["$valutazione", range[0]]}  {"$lte": ["$valutazione", range[1]]}]},"then": "$valutazione", "else": None}},    "else": None}},
                    "valutazione": "$valutazione",
                    "report": 1
                }
            },
            {"$match": {"year": year, "month": month, "day": day, "valutazione": {"$gte": range[0], "$lte": range[1]}}},
            {
                "$group": {
                    "_id": "$name",
                    "valutazione": {"$first": "$valutazione"},
                    "year": {"$first": year},
                    "month": {"$first": month},
                    "day": {"$first": day},
                    "report": {"$first": "$report"}

                }
            }

        ]):
            lista.append(z)
        return lista

        # return year(x) average reports

    def retrieve_year_average_name(self, year, name, range):
        # TODO: ritornare tutti i report medi dell'anno x ogni sito
        # Attualmente: Nel db ho inserito tutte macchine, la media è sull'anno all'interno dell'oggetto obj
        lista = []
        for z in self.collection.aggregate([
            {
                "$project": {
                    "year": {"$year": "$date"},
                    "name": 1,
                    "average": "$valutazione",
                }
            },
            {"$match": {"year": year, "name": name}},
            {
                "$group": {
                    "_id": "$name",
                    "valutazione": {"$avg": "$average"},
                    "year": {"$first": year},
                }
            }, {"$addFields": {
                "valutazione": {"$trunc": ["$valutazione", 2]},
            }},
            {"$match": {"valutazione": {"$gte": range[0], "$lte": range[1]}}}
        ]):
            lista.append(z)
        return lista

        # return month(x) of the year(x) average reports

    def retrieve_month_year_average_name(self, year, month, name, range):
        # TODO: ritornare tutti i report medi del mese x dell'anno x per ogni sito
        # Ci sono due match perchè se il controllo del range sarebbe stato nel primo, nel calcolo della media avrebbe escluso i campi fuori dal range
        # In questo modo, invece, escludo la valutazione media
        lista = []
        for z in self.collection.aggregate([
            {
                "$project": {
                    "year": {"$year": "$date"},
                    "month": {"$month": "$date"},
                    "name": 1,
                    "average": "$valutazione",
                }
            },
            {"$match": {"year": year, "month": month, "name": name}},
            {
                "$group": {
                    "_id": "$name",
                    "valutazione": {"$avg": "$average"},
                    "year": {"$first": year},
                    "month": {"$first": month}
                }
            }, {"$addFields": {
                "valutazione": {"$trunc": ["$valutazione", 2]},
            }},
            {"$match": {"valutazione": {"$gte": range[0], "$lte": range[1]}}}
        ]):
            lista.append(z)
        return lista

        # return day(x) of month(x) of the year(x) average reports

    def retrieve_day_month_year_name(self, year, month, day, name):
        # TODO: ritornare tutti i report del giorno x del mese x dell'anno x per ogni sito
        lista = []
        for z in self.collection.aggregate([
            {
                "$project": {
                    "year": {"$year": "$date"},
                    "month": {"$month": "$date"},
                    "day": {"$dayOfMonth": "$date"},
                    "name": 1,
                    # "valutazione": {"$cond": {"if": { "$and": [{"$ne": [range[0], 0]}, {"$ne": [range[1], 0]}, {"$lt": [range[0], 4]},{"$lt": [range[1], 4]}]},"then": {"$cond": {"if": {"$and": [{"$gte": ["$valutazione", range[0]]}  {"$lte": ["$valutazione", range[1]]}]},"then": "$valutazione", "else": None}},    "else": None}},
                    "valutazione": "$valutazione",
                    "report": 1
                }
            },
            {"$match": {"year": year, "month": month, "day": day,
                        "name": name}},
            {
                "$group": {
                    "_id": "$name",
                    "valutazione": {"$first": "$valutazione"},
                    "year": {"$first": year},
                    "month": {"$first": month},
                    "day": {"$first": day},
                    "report": {"$first": "$report"}

                }
            }

        ]):
            lista.append(z)
        return lista
