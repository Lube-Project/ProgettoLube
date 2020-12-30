# TODO: DJANGO ENVIRONMENT OR FLASK
# per eseguire flask server : python Server.py nel terminale
import pymongo

import flask
from flask import request
from flask_restplus import Api, Resource, fields

from DBmanager import DBmanager

flask_app = flask.Flask(__name__)
app = Api(app=flask_app,
          version="1.0",
          title="Lube reseller websites reports",
          description="Provide some useful api in order to have reports of resellers websites",
          doc='/api-doc/', )

name_space = app.namespace('reports', description='Provide reports')
db_manager = DBmanager()
db_manager.start_connection()
resource_fields = app.model('Report', {
    'year': fields.Integer,
    'range1': fields.Float,
    'range2': fields.Float,
})


# app.config["DEBUG"] = True
@name_space.route('/retrieveLastReports')
class retrieveLastReports(Resource):

    @app.doc(responses={200: 'OK', }, description='Provide all last reports')
    def get(self):
        lista = db_manager.retrieve_last()
        for x in lista:
            x['date'] = x['date'].date()
            x['date'] = x['date'].isoformat()
        return {"lista": lista}


# @app.route('/retrieveYearAverage', methods=['GET'])
@name_space.route('/retrieveYearAverage')
class retrieveYearAverage(Resource):
    @app.doc(responses={200: 'OK', },
             params={'year': {'description': 'Specify the year of the reports', 'type': 'int', 'required': True},
                     'range1': {'description': "Specify the minimum evaluation's range number of the reports",
                                'type': 'float', 'required': True},
                     'range2': {'description': "Specify the maximum evaluation's range number of the reports",
                                'type': 'float', 'required': True}},
             description='Provide all average reports on a specified year', )
    def get(self):
        year = request.args.get('year', type=int)
        range1 = request.args.get('range1', type=float)
        range2 = request.args.get('range2', type=float)
        range = [range1, range2]
        lista = db_manager.retrieve_year_average(year, range)
        return {"lista": lista}


# @app.route('/retrieveMonthYearAverage', methods=['GET'])
@name_space.route('/retrieveMonthYearAverage')
class retrieveMonthYearAverage(Resource):

    @app.doc(responses={200: 'OK', },
             params={'year': {'description': 'Specify the year of the reports', 'type': 'int', 'required': True},
                     'month': {'description': 'Specify the month of the reports', 'type': 'int', 'required': True},
                     'range1': {'description': "Specify the minimum evaluation's range number of the reports",
                                'type': 'float', 'required': True},
                     'range2': {'description': "Specify the maximum evaluation's range number of the reports",
                                'type': 'float', 'required': True}},
             description='Provide all average reports on a specified month in a fixed year')
    def get(self):
        year = request.args.get('year', type=int)
        month = request.args.get('month', type=int)
        range1 = request.args.get('range1', type=float)
        range2 = request.args.get('range2', type=float)
        range = [range1, range2]
        lista = db_manager.retrieve_month_year_average(year, month, range)
        return {"lista": lista}


# @app.route('/retrieveDayMonthYear', methods=['GET'])
@name_space.route('/retrieveDayMonthYear')
class retrieveDayMonthYear(Resource):

    @app.doc(responses={200: 'OK', },
             params={'year': {'description': 'Specify the year of the reports', 'type': 'int', 'required': True},
                     'month': {'description': 'Specify the month of the reports', 'type': 'int', 'required': True},
                     'day': {'description': 'Specify the day of the reports', 'type': 'int', 'required': True},
                     'range1': {'description': "Specify the minimum evaluation's range number of the reports",
                                'type': 'float', 'required': True},
                     'range2': {'description': "Specify the maximum evaluation's range number of the reports",
                                'type': 'float', 'required': True}},
             description='Provide all reports on a precise date')
    def get(self):
        year = request.args.get('year', type=int)
        month = request.args.get('month', type=int)
        day = request.args.get('day', type=int)
        range1 = request.args.get('range1', type=float)
        range2 = request.args.get('range2', type=float)
        range = [range1, range2]
        lista = db_manager.retrieve_day_month_year(year, month, day, range)
        return {"lista": lista}


# @app.route('/retrieveYearAverageName', methods=['GET'])
@name_space.route('/retrieveYearAverageName')
class retrieveYearAverageName(Resource):

    @app.doc(responses={200: 'OK', },
             params={'year': {'description': 'Specify the year of the reports', 'type': 'int', 'required': True},
                     'name': {'description': 'Indicate the name of the reseller', 'type': 'string', 'required': True},
                     'range1': {'description': "Specify the minimum evaluation's range number of the reports",
                                'type': 'float', 'required': True},
                     'range2': {'description': "Specify the maximum evaluation's range number of the reports",
                                'type': 'float', 'required': True}},
             description='Provide all average reports on a specified year of a particular reseller')
    def get(self):
        year = request.args.get('year', type=int)
        name = request.args.get('name', type=str)
        range1 = request.args.get('range1', type=float)
        range2 = request.args.get('range2', type=float)
        range = [range1, range2]
        lista = db_manager.retrieve_year_average_name(year, name, range)
        return {"lista": lista}


# @app.route('/retrieveMonthYearAverageName', methods=['GET'])
@name_space.route('/retrieveMonthYearAverageName')
class retrieveMonthYearAverageName(Resource):

    @app.doc(responses={200: 'OK', },
             params={'year': {'description': 'Specify the year of the reports', 'type': 'int', 'required': True},
                     'month': {'description': 'Specify the month of the reports', 'type': 'int', 'required': True},
                     'name': {'description': 'Indicate the name of the reseller', 'type': 'string', 'required': True},
                     'range1': {'description': "Specify the minimum evaluation's range number of the reports",
                                'type': 'float', 'required': True},
                     'range2': {'description': "Specify the maximum evaluation's range number of the reports",
                                'type': 'float', 'required': True}},
             description='Provide all average reports on a specified month in a fixed year of a particular reseller')
    def get(self):
        year = request.args.get('year', type=int)
        month = request.args.get('month', type=int)
        name = request.args.get('name', type=str)
        range1 = request.args.get('range1', type=float)
        range2 = request.args.get('range2', type=float)
        range = [range1, range2]
        lista = db_manager.retrieve_month_year_average_name(year, month, name, range)
        return {"lista": lista}


# @app.route('/retrieveDayMonthYearName', methods=['GET'])
@name_space.route('/retrieveDayMonthYearName')
class retrieveDayMonthYearName(Resource):

    @app.doc(responses={200: 'OK', },
             params={'year': {'description': 'Specify the year of the reports', 'type': 'int', 'required': True},
                     'month': {'description': 'Specify the month of the reports', 'type': 'int', 'required': True},
                     'day': {'description': 'Specify the day of the reports', 'type': 'int', 'required': True},
                     'name': {'description': 'Indicate the name of the reseller', 'type': 'string',
                              'required': True}, },
             description='Provide a report on a precise date of a particular reseller')
    def get(self):
        year = request.args.get('year', type=int)
        month = request.args.get('month', type=int)
        day = request.args.get('day', type=int)
        name = request.args.get('name', type=str)
        lista = db_manager.retrieve_day_month_year_name(year, month, day, name)
        return {"lista": lista}


# TODO: other api rest

# app.run()


if __name__ == '__main__':
    flask_app.run(debug=True)
