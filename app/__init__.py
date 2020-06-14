import os 

from flask import Flask, request, current_app, send_file
from app.api.writer import write_covid_testing_observations
from app.api.reader import TestingReader
from .api import api_bp
from .client import client_bp

app = Flask(__name__, static_folder='../dist/static')
app.register_blueprint(api_bp)
app.register_blueprint(client_bp)

reader = TestingReader()

from .config import Config
app.logger.info('>>> {}'.format(Config.FLASK_ENV))

@app.route('/')
def index_client():
    dist_dir = current_app.config['DIST_DIR']
    entry = os.path.join(dist_dir, 'index.html')
    return send_file(entry)

@app.route('/testing/write', methods = ['POST'])
def write():
    secret = request.args['secret'] if 'secret' in request.args else None
    try:
        if secret == os.getenv('COVID_WRITE_SECRET'):
            return write_covid_testing_observations()
    except Exception as e:
        return "Error encountered: " + str(e)
    return "Open sesame"

@app.route('/testing/countries')
def get_country_names():
    return reader.get_country_names()

@app.route('/testing/observations_for_country')
def read_observations_for_country():
    country = request.args.get("country")
    return reader.get_observations_for_country(country)


