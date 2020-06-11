import os 

from flask import Flask, request
from server.writer import write_covid_testing_observations
from server.reader import TestingReader

app = Flask(__name__)
reader = TestingReader()

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/testing/write')
def write():
    return write_covid_testing_observations()

@app.route('/testing/countries')
def get_country_names():
    return reader.get_country_names()

@app.route('/testing/observations_for_country')
def read_observations_for_country():
    country = request.args.get("country")
    return reader.get_observations_for_country(country)


