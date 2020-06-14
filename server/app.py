import os 

from flask import Flask, request
from server.writer import write_covid_testing_observations
from server.reader import TestingReader

app = Flask(__name__)
reader = TestingReader()

@app.route('/')
def home():
    return "Ready to process requests..."

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


