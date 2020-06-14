from tinydb import TinyDB, Query

class TinyDBDriver:

    def __init__(self):
        self.db = TinyDB('covid.json')
        self.table_1="testing_stats_1"
        self.table_2="testing_stats_2"
        self.primary_table=None
        self.secondary_table=None

    def get_db(self):
        return self.db

    def determine_table_names(self):
        tables = self.db.tables()
        print(">>>>>>>>>>>")
        print(tables)
        print(">>>>>>>>>>>")
        response = {}
        if self.table_2 in tables:
            self.primary_table = self.table_2
            self.secondary_table = self.table_1
        else:
            self.primary_table = self.table_1
            self.secondary_table = self.table_2
    
    def get_primary_table(self):
        return self.primary_table

    def write_to_tinydb(self, payloads):
        self.determine_table_names()
        print("Before writing records :: Primary table = " + self.primary_table + ", Secondary table = "+ self.secondary_table)
        print("Creating new table => "+ self.secondary_table)
        table = self.db.table(self.secondary_table)
        table.insert_multiple(payloads)
        print("Inserted " + str(len(payloads)) + " records into " + self.secondary_table)
        self.db.drop_table(self.primary_table)
        print("Dropped older table =>"+ self.primary_table)
        temp_table = self.secondary_table
        self.secondary_table = self.primary_table
        self.primary_table = temp_table
        print("After writing records :: Primary table = " + self.primary_table + ", Secondary table = "+ self.secondary_table)
        return {
            "table": self.primary_table,
            "count": len(table.all())
        }
