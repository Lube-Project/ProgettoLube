# TODO: DJANGO ENVIRONMENT OR FLASK
# per eseguire flask server : python Server.py nel terminale

import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "CIAOOOO"


@app.route('/reports', methods=['GET'])
def report():
    return "ALL REPORTS"


# TODO: other api rest


app.run()