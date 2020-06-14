from tinydb import TinyDB, Query

from app.db.driver import TinyDBDriver
db = TinyDB('covid.json')
driver = TinyDBDriver()
table = db.table("testing_stats_1")

class TestingReader:
    def __init__(self):
        self.driver = TinyDBDriver()

    def get_country_names(self) -> str:
        countries = set()
        for record in table.all():
            countries.add(record['country_long_name'])
        res = dict.fromkeys(sorted(countries), 0)
        return res

    def get_observations_for_country(self,country:str='Australia') -> str:
        print(driver.get_primary_table())
        Observations = Query()
        print(len(table.all()))
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