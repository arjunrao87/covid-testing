import requests
from contextlib import closing
import csv
import os
import codecs
import time
from algoliasearch.search_client import SearchClient
from airtable import Airtable
from tinydb import TinyDB, Query

db = TinyDB('covid.json')
table = db.table('testing_stats')
client = SearchClient.create(os.getenv('ALGOLIA_APP_ID'), os.getenv('ALGOLIA_WRITE_API_KEY'))
index = client.init_index('covid_test')
airtable = Airtable(os.getenv('AIRTABLE_BASE'), os.getenv('AIRTABLE_TABLE'))
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/testing/covid-testing-all-observations.csv"

def write_covid_testing_observations():
    with closing(requests.get(url, stream=True)) as r:
        reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'), delimiter=',', quotechar='"')
        next(reader)
        start = time.time()
        payloads = []
        for row in reader:
            country_long_name = row[0].split(' - ')[0]
            type_of_test = row[0].split(' - ')[1]
            country_iso_code = row[1]
            row_date = row[2]
            source_url = row[3]
            source_label = row[4]
            notes = row[5]
            cumulative_total = row[6]
            daily_change_cumulative_total = row[7]
            cumulative_total_per_thousand = row[8]
            daily_change_in_cumulative_total_per_thousand = row[9]
            seven_day_smoothed_daily_change = row[10]
            seven_day_smoothed_daily_change_per_thousand = row[11]
            id_val=country_long_name+'_'+row_date
            payload = {
                'id': id_val,
                'country_long_name': country_long_name, 
                'type_of_test': type_of_test,
                'country_iso_code': country_iso_code,
                'row_date': row_date,
                'source_url': source_url,
                'notes': notes,
                'cumulative_total': cumulative_total,
                'daily_change_cumulative_total': daily_change_cumulative_total,
                'cumulative_total_per_thousand': cumulative_total_per_thousand,
                'daily_change_in_cumulative_total_per_thousand': daily_change_in_cumulative_total_per_thousand,
                'seven_day_smoothed_daily_change': seven_day_smoothed_daily_change,
                'seven_day_smoothed_daily_change_per_thousand': seven_day_smoothed_daily_change_per_thousand,
            }
            payloads.append(payload)
            # upsert_record(payload)
        end = time.time()
        table.insert_multiple(payloads)
        print("Inserted record")
        print("Number of records = = " + str(len(table.all())))
        index.save_objects(payloads, {'autoGenerateObjectIDIfNotExist': True})
        return "Done = " + str(end-start)

def upsert_record(payload:str):
    record=airtable.match('id', payload['id'])
    if not record:
        airtable.insert(payload)
    else:
        airtable.update_by_field('id', payload['id'],payload)
