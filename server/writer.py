import requests
from contextlib import closing
from server.db.driver import TinyDBDriver
import csv
import os
import codecs
import time

url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/testing/covid-testing-all-observations.csv"
driver = TinyDBDriver()

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
        end = time.time()
        response = driver.write_to_tinydb(payloads)
        return "Wrote " + str(response["count"]) + " into table=" + response["table"] + " in " + str(end-start) + " seconds."
