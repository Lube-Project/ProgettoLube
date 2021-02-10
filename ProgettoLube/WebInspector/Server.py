# TODO: DJANGO ENVIRONMENT OR FLASK
# per eseguire flask server : python Server.py nel terminale
import pymongo
import json
import flask
from flask import request, jsonify
from flask import render_template
from flask_restplus import Api, Resource, fields
from flask_cors import CORS

import DashboardConfig
from DBmanager import DBmanager
from bson.objectid import ObjectId
from LoadResources import LoadResources

flask_app = flask.Flask(__name__)
app = Api(app=flask_app,
          version="1.0",
          title="Lube reseller websites reports",
          description="Provide some useful api in order to have reports of resellers websites",
          doc='/api-doc/', )
CORS(flask_app)
name_space = app.namespace('reportsWeb', description='Provide web reports')
name_spacetwo = app.namespace('reportsFacebook', description='Provide facebook reports')
name_spacethree = app.namespace('reportsInstagram', description='Provide instagram reports')
name_space_resources = app.namespace('resellers', description='Provide resellers info')
dashboard_settings = app.namespace('settings', description='Provide methods to modify settings of dashboard')
db_manager = DBmanager()
db_manager.start_connection()
resource_fields = app.model('Report', {
    'year': fields.Integer,
    'range1': fields.Float,
    'range2': fields.Float,
})


######################################### LOAD RESOURCES ##############################################################
@name_space_resources.route('/retrieveResellersNames')
class retrieveResellersNames(Resource):

    @app.doc(responses={200: 'OK', }, description='Provide resellers names')
    def get(self):
        load = LoadResources()
        lista = load.load_name_resellers()
        return {"lista": lista}


@name_space_resources.route('/retrieveResellersPositions')
class retrieveResellersPositions(Resource):

    @app.doc(responses={200: 'OK', }, description='Provide resellers positions')
    def get(self):
        load = LoadResources()
        lista = load.load_store_positions()
        return {"lista": lista}


@name_space_resources.route('/retrieveResellerDetails')
class retrieveResellerDetails(Resource):

    @app.doc(responses={200: 'OK', }, description='Provide reseller details',
             params={'name': {'description': "Specify the reseller's name", 'type': 'string', 'required': True}})
    def get(self):
        name = request.args.get('name', type=str)
        load = LoadResources()
        dict = load.load_store_details_name(name)
        return dict


######################################################################################################################à

# app.config["DEBUG"] = True
@name_space.route('/retrieveLastReports')
class retrieveLastReports(Resource):

    @app.doc(responses={200: 'OK', }, description='Provide all last reports')
    def get(self):
        lista = db_manager.retrieve_last()
        for x in lista:
            x['date'] = x['date'].date()
            x['date'] = x['date'].isoformat()
        for y in lista:
            y['id'] = str(y['id'])
        return {"lista": lista}


@name_space.route('/findOne')
class findOne(Resource):
    @app.doc(responses={200: 'OK', },
             params={'id': {'description': 'Specify the id of the report', 'type': 'int', 'required': True}, }
        , description='find specific report by id')
    def get(self):
        id = request.args.get('id', type=str)
        lista = db_manager.find_one(ObjectId(id))
        for x in lista:
            x['date'] = x['date'].date()
            x['date'] = x['date'].isoformat()
        for y in lista:
            y['id'] = str(y['id'])
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
############################################ SETTINGS #####################################################
@dashboard_settings.route('/getKeywordsCrawler')
class retrieveKeywordsCrawler(Resource):

    @app.doc(responses={200: 'OK', },
             description='Provide all keywords that the Crawlers use to analyze')
    def get(self):
        lista = list(dict.fromkeys(DashboardConfig.keywordsCrawler))
        return {"lista": lista}


@dashboard_settings.route('/addKeywordCrawler')
class addKeywordCrawler(Resource):

    @app.doc(responses={200: 'OK', },
             params={'keyword': {'description': 'new keyword to be used by the Crawlers', 'type': 'string',
                                 'required': True}, },
             description='Method to add a new keyword')
    def get(self):
        keyword = request.args.get('keyword', type=str)
        DashboardConfig.keywordsCrawler.append(keyword)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@dashboard_settings.route('/deleteKeywordCrawler')
class removeKeywordCrawler(Resource):

    @app.doc(responses={200: 'OK', },
             params={'keyword': {'description': 'keyword to be removed', 'type': 'string',
                                 'required': True}, },
             description='Method to remove a keyword')
    def get(self):
        keyword = request.args.get('keyword', type=str)
        DashboardConfig.keywordsCrawler.remove(keyword)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@dashboard_settings.route('/getKeywordsCrawlerSocial')
class retrieveKeywordsCrawlerSocial(Resource):

    @app.doc(responses={200: 'OK', },
             description='Provide all keywords that the Crawlers use to analyze')
    def get(self):
        lista = list(dict.fromkeys(DashboardConfig.keywordsCrawlerSocial))
        return {"lista": lista}


@dashboard_settings.route('/addKeywordCrawlerSocial')
class addKeywordCrawlerSocial(Resource):

    @app.doc(responses={200: 'OK', },
             params={'keyword': {'description': 'new keyword to be used by the Crawlers', 'type': 'string',
                                 'required': True}, },
             description='Method to add a new keyword')
    def get(self):
        keyword = request.args.get('keyword', type=str)
        DashboardConfig.keywordsCrawlerSocial.append(keyword)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@dashboard_settings.route('/deleteKeywordCrawlerSocial')
class removeKeywordCrawlerSocial(Resource):

    @app.doc(responses={200: 'OK', },
             params={'keyword': {'description': 'keyword to be removed', 'type': 'string',
                                 'required': True}, },
             description='Method to remove a keyword')
    def get(self):
        keyword = request.args.get('keyword', type=str)
        DashboardConfig.keywordsCrawlerSocial.remove(keyword)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@dashboard_settings.route('/getSocialActivityTimeCrawler')
class getSocialActivityTimeCrawler(Resource):

    @app.doc(responses={200: 'OK', },
             description="Provides the number of days the crawler monitors the seller's social network")
    def get(self):
        return DashboardConfig.numeroGiorniToCheckOnSocialProfileActivity


@dashboard_settings.route('/modifySocialActivityTimeCrawler')
class modifySocialActivityTimeCrawler(Resource):

    @app.doc(responses={200: 'OK', },
             params={'days': {'description': 'new days number', 'type': 'int',
                              'required': True}, },
             description='Method to remove a keyword')
    def get(self):
        days = request.args.get('days', type=int)
        DashboardConfig.numeroGiorniToCheckOnSocialProfileActivity = days
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


##################################### FACEBOOK #########################################################

# app.config["DEBUG"] = True
@name_spacetwo.route('/retrieveLastReportsFacebook')
class retrieveLastReportsFacebook(Resource):

    @app.doc(responses={200: 'OK', }, description='Provide all last reports')
    def get(self):
        lista = db_manager.retrieve_last_facebook()
        for x in lista:
            x['date'] = x['date'].date()
            x['date'] = x['date'].isoformat()
        for y in lista:
            y['id'] = str(y['id'])
        return {"lista": lista}


@name_spacetwo.route('/findOneFacebook')
class findOneFacebook(Resource):
    @app.doc(responses={200: 'OK', },
             params={'id': {'description': 'Specify the id of the report', 'type': 'int', 'required': True}, }
        , description='find specific report by id')
    def get(self):
        id = request.args.get('id', type=str)
        lista = db_manager.find_one_facebook(ObjectId(id))
        for x in lista:
            x['date'] = x['date'].date()
            x['date'] = x['date'].isoformat()
        for y in lista:
            y['id'] = str(y['id'])
        return {"lista": lista}


##################################### INSTAGRAM #########################################################

# app.config["DEBUG"] = True
@name_spacethree.route('/retrieveLastReportsInstagram')
class retrieveLastReportsInstagram(Resource):

    @app.doc(responses={200: 'OK', }, description='Provide all last reports')
    def get(self):
        lista = db_manager.retrieve_last_instagram()
        for x in lista:
            x['date'] = x['date'].date()
            x['date'] = x['date'].isoformat()
        for y in lista:
            y['id'] = str(y['id'])
        return {"lista": lista}


@name_spacethree.route('/findOneInstagram')
class findOneInstagram(Resource):
    @app.doc(responses={200: 'OK', },
             params={'id': {'description': 'Specify the id of the report', 'type': 'int', 'required': True}, }
        , description='find specific report by id')
    def get(self):
        id = request.args.get('id', type=str)
        lista = db_manager.find_one_instagram(ObjectId(id))
        for x in lista:
            x['date'] = x['date'].date()
            x['date'] = x['date'].isoformat()
        for y in lista:
            y['id'] = str(y['id'])
        return {"lista": lista}


# app.run()


if __name__ == '__main__':
    flask_app.run(debug=True)
