import csv
import os
import codecs
import time
import requests

from contextlib import closing
from tinydb import Query
from app.db.driver import TinyDBDriver


url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/testing/covid-testing-all-observations.csv"
driver = TinyDBDriver()

def write_covid_testing_observations() -> str:
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

def get_metrics_details() -> str:
    response = [
        {
            'name': 'Cumulative Total',
            'label': 'cumulative_total',
            'color': 'rgba(165, 107, 223,0.4)'
        },
        {
            'name': 'Daily Change in Cumulative Total',
            'label': 'daily_change_cumulative_total',
            'color': 'rgba(223, 107, 107,0.4)'
        },
        {
            'name': 'Cumulative Total per 1000',
            'label': 'cumulative_total_per_thousand',
            'color': 'rgba(17, 96, 186, 0.2)'
        },
        {
            'name': 'Daily Change in cumulative total per 1000',
            'label': 'daily_change_in_cumulative_total_per_thousand',
            'color': 'rgba(255,153,0,0.4)',
        },
        {
            'name': '7-day smoothed daily change',
            'label': 'seven_day_smoothed_daily_change',
            'color': 'rgba(255, 220, 244,0.4)'
        },
        {
            'name': '7-day smoothed daily change per 1000',
            'label': 'seven_day_smoothed_daily_change_per_thousand',
            'color': 'rgba(220, 255, 251,0.4)'
        }
    ]
    return {
        'values': response
    }

def get_country_names():
    table = driver.get_db().table(driver.get_primary_table())
    countries = set()
    for record in table.all():
        countries.add(record['country_long_name'])
    res = dict.fromkeys(sorted(countries), 0)
    return res

def get_observations_for_country(country:str='Australia'):
    table = driver.get_db().table(driver.get_primary_table())
    Observations = Query()
    rows = table.search(Observations.country_long_name == country)
    data = {
        "row_date": [],
        "cumulative_total": [],
        "daily_change_cumulative_total": [],
        "cumulative_total_per_thousand": [],
        "daily_change_in_cumulative_total_per_thousand": [],
        "seven_day_smoothed_daily_change": [],
        "seven_day_smoothed_daily_change_per_thousand": [],
    }
    for row in rows:
        data["row_date"].append(row["row_date"])
        data["cumulative_total"].append(row["cumulative_total"])
        data["daily_change_cumulative_total"].append(row["daily_change_cumulative_total"])
        data["cumulative_total_per_thousand"].append(row["cumulative_total_per_thousand"])
        data["daily_change_in_cumulative_total_per_thousand"].append(row["daily_change_in_cumulative_total_per_thousand"])
        data["seven_day_smoothed_daily_change"].append(row["seven_day_smoothed_daily_change"])
        data["seven_day_smoothed_daily_change_per_thousand"].append(row["seven_day_smoothed_daily_change_per_thousand"])
    return data