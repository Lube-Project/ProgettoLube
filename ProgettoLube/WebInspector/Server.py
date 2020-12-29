# TODO: DJANGO ENVIRONMENT OR FLASK
# per eseguire flask server : python Server.py nel terminale
import pymongo
import flask
from flask import request

from DBmanager import DBmanager

db_manager = DBmanager()
db_manager.start_connection()

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/retrieveLastReports', methods=['GET'])
def retrieveLastReports():
    lista = db_manager.retrieve_last()
    return {"lista": lista}


@app.route('/retrieveYearAverage', methods=['GET'])
def retrieveYearAverage():
    year = request.args.get('year', type=int)
    range1 = request.args.get('range1', type=int)
    range2 = request.args.get('range2', type=int)
    range = [range1, range2]
    lista = db_manager.retrieve_year_average(year,range)
    return {"lista": lista}


@app.route('/retrieveMonthYearAverage', methods=['GET'])
def retrieveMonthYearAverage():
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    range1 = request.args.get('range1', type=int)
    range2 = request.args.get('range2', type=int)
    range = [range1, range2]
    lista = db_manager.retrieve_month_year_average(year, month, range)
    return {"lista": lista}


@app.route('/retrieveDayMonthYear', methods=['GET'])
def retrieveDayMonthYear():
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    day = request.args.get('day', type=int)
    range1 = request.args.get('range1', type=int)
    range2 = request.args.get('range2', type=int)
    range = [range1, range2]
    lista = db_manager.retrieve_day_month_year(year, month, day, range)
    return {"lista": lista}


@app.route('/retrieveYearAverageName', methods=['GET'])
def retrieveYearAverageName():
    year = request.args.get('year', type=int)
    name = request.args.get('name', type=str)
    range1 = request.args.get('range1', type=int)
    range2 = request.args.get('range2', type=int)
    range = [range1, range2]
    lista = db_manager.retrieve_year_average_name(year, name, range)
    return {"lista": lista}


@app.route('/retrieveMonthYearAverageName', methods=['GET'])
def retrieveMonthYearAverageName():
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    name = request.args.get('name', type=str)
    range1 = request.args.get('range1', type=int)
    range2 = request.args.get('range2', type=int)
    range = [range1, range2]
    lista = db_manager.retrieve_month_year_average_name(year, month, name, range)
    return {"lista": lista}


@app.route('/retrieveDayMonthYearName', methods=['GET'])
def retrieveDayMonthYearName():
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    day = request.args.get('day', type=int)
    name = request.args.get('name', type=str)
    lista = db_manager.retrieve_day_month_year_name(year, month, day, name)
    return {"lista": lista}































# TODO: other api rest


app.run()
