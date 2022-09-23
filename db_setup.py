import shared
import zipfile
import os

# create intial CIM900 data table
sql_db = shared.create_connection("cim900.db")
shared.create_table(
    sql_db,
    "CREATE TABLE IF NOT EXISTS cim900_data (_data text);",
)

# create view for branches
shared.create_table(
    sql_db,
    "CREATE VIEW IF NOT EXISTS view_branch_details AS select distinct trim(substr(_data,3,6)) AS branch_no,trim(substr(_data,9,30)) AS branch_name,(case when (trim(substr(_data,9,30)) like '%closed%') then 'Y' else 'N' end) AS Closed,trim(substr(_data,39,30)) AS member_name,trim(substr(_data,77,6)) AS member_no,trim(substr(_data,273,35)) AS country from cim900_data;",
)

# extract CIM900.zip
with zipfile.ZipFile("CIM900.zip", "r") as zip_ref:
    zip_ref.extractall(".")

# read CIM900 file
with open("CIM900", "r") as f:
    data = f.readlines()

# remove file
os.remove("CIM900")

# insert data into table
shared.insert_data_many(
    sql_db,
    "INSERT OR IGNORE INTO cim900_data VALUES (?);",
    [(x,) for x in data],
)

if __name__ == "__main__":
    import pprint

    pprint.pprint(
        shared.select_data(sql_db, "SELECT * FROM view_branch_details limit 5;")
    )
