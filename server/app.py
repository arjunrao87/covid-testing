import os 

from flask import Flask, request
from src.writer import write_covid_testing_observations

app = Flask(__name__)

@app.route('/testing/write')
def home():
    return write_covid_testing_observations()

@app.route('/testing/observations_for_country')
def home():
    return write_covid_testing_observations()


