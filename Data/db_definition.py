import sqlite3
from sqlite3 import Error

DBNAME = "register.db"


class DB:

    # noinspection PyMethodMayBeStatic
    def create_table(self, qry):
        connect(new_table, qry)

    # noinspection PyMethodMayBeStatic
    def fill_dictionary(self, table, items):
        connect(fill_dict_tables, table, items)

    # noinspection PyMethodMayBeStatic
    def if_empty_is_empty(self, table):
        result = is_empty(check_table, table)
        return result

    @staticmethod
    def get_connection():
        conn = create_connection(DBNAME)
        if conn is not None:
            return conn
        else:
            return None


def create_connection(db_name):
    """ create a database connection to a given SQLite database """
    try:
        conn = sqlite3.connect(db_name)
        return conn
    except Error as e:
        print(e)
        return None


# Higher Order Function
def connect(function, sql, items=None):
    conn = DB.get_connection()
    try:
        if items is not None:
            function(conn, sql, items)
        else:
            function(conn, sql)
    except Error as e:
        print(e)
    finally:
        conn.close()


def is_empty(check_function, table):
    conn = DB.get_connection()
    rows = 0
    try:
        if conn is not None:
            rows = check_function(conn, table)
    except Error as e:
        print(e)
    finally:
        conn.close()
        return rows[0]


def new_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        return True
    except Error as e:
        print(e)
        return False


def fill_dict_tables(conn, table, items):
    """
    Create a new project into the projects table
    :param conn:
    :param table:
    :param items:
    """
    cur = conn.cursor()
    for item in items:
        query = 'INSERT OR IGNORE INTO ' + table + ' VALUES ("' + item + '")'
        cur.execute(query)
    conn.commit()
    return cur.lastrowid


def check_table(conn, table):
    cursor = conn.cursor()
    sql = f"SELECT count(*) as Total FROM {table}"
    cursor.execute(sql)
    data = cursor.fetchone()
    return data
