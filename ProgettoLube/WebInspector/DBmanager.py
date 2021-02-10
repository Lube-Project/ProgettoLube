# TODO: RICORDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA che il nome in input ai metodi va controllato lato frontend dandogli al medesimo la tabella excel
# TODO:FARE menu a tendina dove mostri tutti i nomi dei siti, così non bisogna controllare la validità del nome
# TODO: RICORDAAA DI CONTROLLARE IL RANGE DELLA VALUTAZIONE LATO FRONTEND: !=0 AND <4

import pymongo
import datetime


class DBmanager:
    client = None
    db = None
    collection = None
    collection_keyword = None
    collection_facebook = None
    collection_instagram = None

    def start_connection(self):
        self.client = pymongo.MongoClient(
            "mongodb+srv://molciprom:molciprom@clusterlube.auwyr.mongodb.net/lube_reports?retryWrites=true&w=majority")
        self.db = self.client["lube_reports"]
        self.collection = self.db["web_reports"]
        self.collection_facebook = self.db["facebook_reports"]
        self.collection_instagram = self.db["instagram_reports"]

    def insert(self, report):
        # print(report.toJSON())
        # x = self.collection.insert_one(report.toJSON())
        date = datetime.datetime.now()
        report['date'] = date
        x = self.collection.insert_one(report)

    def find_all(self):
        lista = []
        for x in self.collection.find():
            lista.append(x)
        return lista

    def find_one(self, id):
        lista = []
        for z in self.collection.aggregate([
            {
                "$project": {
                    "_id": 0,
                    "id": "$_id",
                    "date": 1,
                    "report_foto": 1,
                    "report_pagine": 1,
                    "sito": 1,
                    "valutazione_foto": 1,
                    "valutazione_script": 1,
                    "valutazione_keywords": 1
                }
            },
            {"$match": {"id": id}},
        ]):
            lista.append(z)
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
                    "id": "$_id",
                    "date": 1,
                    "report_foto": 1,
                    "report_pagine": 1,
                    "sito": 1,
                    "valutazione_foto": 1,
                    "valutazione_script": 1,
                    "valutazione_keywords": 1
                }
            },
            {"$match": {"date": date}},
        ]):
            lista.append(z)
        return lista

    ######################### DETTAGLI SITO ###########################################
    # return year(x) documents
    def retrieve_yearly_historic_of_store(self, name, year, range):
        # TODO: fare report medio su 365 usando il campo valutazione o se si riesce anche gli altri campi e tornare anche tutti i relativi report
        lista = self.retrieve_year_average_name(year, name, range)
        for z in self.collection.aggregate([
            {
                "$project": {
                    "_id": 0,
                    "id": "$_id",
                    "year": {"$year": "$date"},
                    "report": 1,
                    "name": 1,
                    "valutazione": 1
                }
            },
            {"$match": {"name": name,
                        "year": year,
                        "valutazione": {"$gte": range[0], "$lte": range[1]}}},
        ]):
            lista.append(z)
        return lista

    # return month(x) of the year(x) documents
    def retrieve_monthly_historic_of_store(self, name, month, year, range):
        # TODO: fare report medio su numero report usando il campo valutazione o se si riesce anche gli altri campi e tornare anche tutti i relativi report
        lista = self.retrieve_month_year_average_name(year, month, name, range)
        for z in self.collection.aggregate([
            {
                "$project": {
                    "_id": 0,
                    "id": "$_id",
                    "year": {"$year": "$date"},
                    "month": {"$month": "$date"},
                    "report": 1,
                    "name": 1,
                    "valutazione": 1
                }
            },
            {"$match": {"name": name,
                        "year": year,
                        "month": month,
                        "valutazione": {"$gte": range[0], "$lte": range[1]}}},
        ]):
            lista.append(z)
        return lista

    # return day-month-year(x) documents
    def retrieve_daily_historic_of_store(self, name, year, month, day):
        # TODO: stuff
        lista = self.retrieve_day_month_year_name(year, month, day, name)
        for z in self.collection.aggregate([
            {
                "$project": {
                    "_id": 0,
                    "id": "$_id",
                    "year": {"$year": "$date"},
                    "month": {"$month": "$date"},
                    "day": {"$dayOfMonth": "$date"},
                    "report": 1,
                    "name": 1,
                    "valutazione": 1
                }
            },
            {"$match": {"name": name,
                        "year": year,
                        "month": month,
                        "day": day, }}
        ]):
            lista.append(z)
        return lista

    ################################## HOME #################################################

    # return year(x) average reports
    def retrieve_year_average(self, year, range):
        # TODO: ritornare tutti i report medi dell'anno x ogni sito
        # Attualmente: Nel db ho inserito tutte macchine, la media è sul
        # l'anno all'interno dell'oggetto obj
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
                    "id": {"$first": "$name"},
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
                    "id": {"$first": "$name"},
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
                    "id": {"$first": "$name"},
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
                    "id": {"$first": "$name"},
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
                    "id": {"$first": "$name"},
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
                    "id": {"$first": "$name"},
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

    ##################################################### FACEBOOK ######################################################

    def insert_facebook_report(self, report):
        # print(report.toJSON())
        # x = self.collection.insert_one(report.toJSON())
        date = datetime.datetime.now()
        report['date'] = date
        x = self.collection_facebook.insert_one(report)

    def find_one_facebook(self, id):
        lista = []
        for z in self.collection_facebook.aggregate([
            {
                "$project": {
                    "_id": 0,
                    "id": "$_id",
                    "date": 1,
                    "report_foto": 1,
                    "dictionary_parolechiave_nel_post": 1,
                    "social": 1,
                    "nome": 1,
                    "quantita_post_neltempo":1,
                    "valutazione_foto": 1,
                    "valutazione_keywords": 1
                }
            },
            {"$match": {"id": id}},
        ]):
            lista.append(z)
        return lista

    # return last document
    def retrieve_last_facebook(self):
        sup = []
        lista = []
        date = []
        for x in self.collection_facebook.find({}).sort([("date", -1)]).limit(1):
            sup.append(x)
        date = x['date']
        # for x in self.collection.find({"date": date}, {"_id": 0, "date": 1, "report": 1, "name": 1, "valutazione": 1}):
        # lista.append(x)
        for z in self.collection_facebook.aggregate([
            {
                "$project": {
                    "_id": 0,
                    "id": "$_id",
                    "date": 1,
                    "report_foto": 1,
                    "dictionary_parolechiave_nel_post": 1,
                    "social": 1,
                    "nome": 1,
                    "quantita_post_neltempo":1,
                    "valutazione_foto": 1,
                    "valutazione_keywords": 1
                }
            },
            {"$match": {"date": date}},
        ]):
            lista.append(z)
        return lista
##################################################### INSTAGRAM ######################################################

    def insert_instagram_report(self, report):
        # print(report.toJSON())
        # x = self.collection.insert_one(report.toJSON())
        date = datetime.datetime.now()
        report['date'] = date
        x = self.collection_instagram.insert_one(report)

    def find_one_instagram(self, id):
        lista = []
        for z in self.collection_instagram.aggregate([
            {
                "$project": {
                    "_id": 0,
                    "id": "$_id",
                    "nome":1,
                    "date": 1,
                    "report_foto": 1,
                    "dictionary_parolechiave_nel_post": 1,
                    "quantita_post_neltempo": 1,
                    "valutazione_foto": 1,
                    "social": 1,
                    "valutazione_keywords": 1
                }
            },
            {"$match": {"id": id}},
        ]):
            lista.append(z)
        return lista

    # return last document
    def retrieve_last_instagram(self):
        sup = []
        lista = []
        date = []
        for x in self.collection_instagram.find({}).sort([("date", -1)]).limit(1):
            sup.append(x)
        date = x['date']
        # for x in self.collection.find({"date": date}, {"_id": 0, "date": 1, "report": 1, "name": 1, "valutazione": 1}):
        # lista.append(x)
        for z in self.collection_instagram.aggregate([
            {
                "$project": {
                    "_id": 0,
                    "id": "$_id",
                    "nome": 1,
                    "date": 1,
                    "report_foto": 1,
                    "dictionary_parolechiave_nel_post": 1,
                    "quantita_post_neltempo": 1,
                    "valutazione_foto": 1,
                    "social": 1,
                    "valutazione_keywords": 1
                }
            },
            {"$match": {"date": date}},
        ]):
            lista.append(z)
        return lista