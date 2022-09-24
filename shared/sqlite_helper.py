import sqlite3


def sqlite_create_connection(db_file):
    """create a database connection to a SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn


def sqlite_create_table(conn, create_table_sql):
    """create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


def sqlite_insert_data_many(conn, insert_data_sql, args):
    """insert data into a table
    :param conn: Connection object
    :param insert_data_sql: a INSERT INTO statement
    :param args: a list of tuples
    :return:
    """
    try:
        c = conn.cursor()
        c.executemany(insert_data_sql, args)
        conn.commit()
    except sqlite3.Error as e:
        print(e)


def sqlite_select_data(conn, select_data_sql):
    """select data from a table
    :param conn: Connection object
    :param select_data_sql: a SELECT statement
    :return:
    """
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
