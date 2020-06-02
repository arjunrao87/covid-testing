import requests
from contextlib import closing
import csv
import os
import codecs
import time
from tinydb import TinyDB, Query

db = TinyDB('covid.json')
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/testing/covid-testing-all-observations.csv"
table_1="testing_stats_1"
table_2="testing_stats_2"
primary_table=None
secondary_table=None

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
        response = write_to_tinydb(payloads)
        return "Wrote " + str(response["count"]) + " into table=" + response["table"] + " in " + str(end-start) + " seconds."

def write_to_tinydb(payloads):
    global primary_table
    global secondary_table
    get_table_names()
    print("Before writing records :: Primary table = " + primary_table + ", Secondary table = "+ secondary_table)
    print("Creating new table => "+ secondary_table)
    table = db.table(secondary_table)
    table.insert_multiple(payloads)
    print("Inserted " + str(len(payloads)) + " records into " + secondary_table)
    db.drop_table(primary_table)
    print("Dropped older table =>"+ primary_table)
    temp_table = secondary_table
    secondary_table = primary_table
    primary_table = temp_table
    print("After writing records :: Primary table = " + primary_table + ", Secondary table = "+ secondary_table)
    return {
        "table": primary_table,
        "count": len(table.all())
    }

def get_table_names():
    global primary_table
    global secondary_table
    tables = db.tables()
    print(">>>>>>>>>>>")
    print(tables)
    print(">>>>>>>>>>>")
    response = {}
    if table_2 in tables:
        primary_table = table_2
        secondary_table = table_1
    else:
        primary_table = table_1
        secondary_table = table_2