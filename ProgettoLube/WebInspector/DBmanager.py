# TODO: connessione con vero database forse mongodb e per testing mongocloud
import pymongo
import datetime



class DBmanager:

    def insert(self, collection, report):
        print(report.toJSON())
        x = collection.insert_one(report.toJSON())

    def delete(self):
        pass

    def update(self):
        pass

    def retrieve_all(self, collection):
        lista = []
        for x in collection.find({}, {"_id": 0, "date": 1, "report": 1}):
            lista.append(x)
        return lista

    # return last document
    def retrieve_last(self, collection):
        sup = []
        lista = []
        date = []
        for x in collection.find({}).sort([("date", -1)]).limit(1):
            sup.append(x)
        date = x['date']
        for x in collection.find({"date": date}, {"_id": 0, "date": 1, "report": 1}):
            lista.append(x)
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
    def retrieve_dayMonthYear(self,collection, year, month, day):
        # TODO: stuff
        pass

    ################################## HOME #################################################

    # return year(x) average reports
    def retrieve_year_average(self, collection, year):
        # TODO: ritornare tutti i report medi dell'anno x ogni sito
        pass

    # return month(x) of the year(x) average reports
    def retrieve_month_year_average(self, collection, year, month):
        # TODO: ritornare tutti i report medi del mese x dell'anno x per ogni sito
        pass

    # return day(x) of month(x) of the year(x) average reports
    def retrieve_day_month_year_average(self, collection, year, month, day):
        # TODO: ritornare tutti i report del giorno x del mese x dell'anno x per ogni sito
        lista = []
        x = datetime.date(year, month, day)
        for x in collection.find({"date": x}, {"_id": 0, "date": 1, "report": 1}):
            lista.append(x)
        return lista
