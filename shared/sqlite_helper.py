import sqlite3

## create a database connection to a SQLite database
# params:
#   db_file: database file
def sqlite_create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn


## create a table from the create_table_sql statement
# params:
#   conn: Connection object
#   create_table_sql: a CREATE TABLE statement
def sqlite_create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


## insert data into a table
# params:
#   conn: Connection object
#   insert_data_sql: a INSERT INTO statement
#   args: data to be inserted
def sqlite_insert_data_many(conn, insert_data_sql, args):
    try:
        c = conn.cursor()
        c.executemany(insert_data_sql, args)
        conn.commit()
    except sqlite3.Error as e:
        print(e)


## insert data into a table
# params:
#   conn: Connection object
#   insert_data_sql: a INSERT INTO statement
def sqlite_select_data(conn, select_data_sql):
    try:
        c = conn.cursor()
        c.row_factory = sqlite3.Row
        values = c.execute(select_data_sql).fetchall()

        list_accumulator = []
        for item in values:
            list_accumulator.append({k: item[k] for k in item.keys()})
        return list_accumulator
    except sqlite3.Error as e:
        print(e)
