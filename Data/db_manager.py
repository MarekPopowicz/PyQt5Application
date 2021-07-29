import Data.db_data as dbData
import Data.db_definition as dbDef
import Data.db_query_commands as dbQry
from sqlite3 import Error

# Set database object reference
DataBase = dbDef.DB()


def create_database():
    """Creates database tables and fills them with initial data"""
    # Create all db tables
    DataBase.create_table(dbQry.SQL_CREATE_USERS_TABLE)
    DataBase.create_table(dbQry.SQL_CREATE_PROJECTS_TABLE)
    DataBase.create_table(dbQry.SQL_CREATE_TASKS_TABLE)
    DataBase.create_table(dbQry.SQL_CREATE_DEVICE_TABLE)
    DataBase.create_table(dbQry.SQL_CREATE_ATTACHMENTS_TABLE)

    # Dictionary tables
    DataBase.create_table(dbQry.SQL_CREATE_PROJECTS_TASKS_TYPES)
    DataBase.create_table(dbQry.SQL_CREATE_STREETS)
    DataBase.create_table(dbQry.SQL_CREATE_PLACES)
    DataBase.create_table(dbQry.SQL_CREATE_DOCUMENTS)
    DataBase.create_table(dbQry.SQL_CREATE_REGULATIONS)
    DataBase.create_table(dbQry.SQL_CREATE_DEVICE_TYPES)

    # Set initial users if table is empty
    # set_init_users()

    # Fill dictionaries tables with data
    DataBase.fill_dictionary("dict_tasks_names", dbData.PROJECTS_TASKS_TYPES)
    DataBase.fill_dictionary("dict_streets_names", dbData.STREETS)
    DataBase.fill_dictionary("dict_places_names", dbData.PLACES)
    DataBase.fill_dictionary("dict_documents_names", dbData.DOCUMENTS)
    DataBase.fill_dictionary("dict_regulations", dbData.REGULATIONS)
    DataBase.fill_dictionary("dict_devices_types", dbData.DEVICE_TYPES)


def set_init_users():
    """Adds initial users into the users table"""
    users = dbData.USERS
    rows = DataBase.if_empty_is_empty("users")
    if rows == 0:
        try:
            for user in users:
                connect(insert, user, dbQry.QUERY_INSERT_USER)
        except Error as e:
            print(e)


def insert(cn, query, item_data):
    """
    Add a new item into the table
    :param query: sql query string to insert item_data
    :param item_data: data tuple
    :param cn: connection object
    :return: last row id
    """
    cur = cn.cursor()

    cur.execute(query, (item_data,))
    cn.commit()
    last_id = cur.lastrowid
    return last_id


def add(cn, query, item_data):
    """
    Add a new item into the table
    :param query: sql query string to insert item_data
    :param item_data: data tuple
    :param cn: connection object
    :return: last row id
    """
    cur = cn.cursor()

    cur.execute(query, item_data)
    cn.commit()
    last_id = cur.lastrowid
    return last_id


def delete(cn, query):
    """
    Delete an item from the table
    :param query: sql query string to insert item_data
    :param cn: connection object
    """
    cur = cn.cursor()
    cur.execute(query)
    cn.commit()
    if cur.rowcount < 1:
        return False
    else:
        return True


def update(cn, query):
    """
    Update an item from the table
    :param query: sql query string to update a single item_data
    :param cn: connection object
    """
    cur = cn.cursor()
    cur.execute(query)
    cn.commit()
    if cur.rowcount < 1:
        return False
    else:
        return True


def select_all(cn, query):
    """
    Grab all items from the table
    :param query: sql query string to select item_data
    :param cn: connection object
    :return: set of rows
    """
    cur = cn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    return result


# Higher Order Function
def connect(function, sql, item=None):
    conn = DataBase.get_connection()
    result = None
    try:
        if item is not None:
            result = function(conn, sql, item)
        else:
            result = function(conn, sql)
    except Error as e:
        print(e)
    finally:
        conn.close()
        return result


def if_user_exists():
    sql = "SELECT count(*) as Total FROM users"
    if connect(check_user_table, sql) == 0:
        return False
    else:
        return True


def check_user_table(conn, qry):
    cursor = conn.cursor()
    cursor.execute(qry)
    data = cursor.fetchone()
    return data


class DBManager:
    def __init__(self):
        create_database()

    @staticmethod
    def add_new_item(qry, itm):
        return connect(insert, qry, itm)

    @staticmethod
    def add_new_items(qry, itm):
        return connect(add, qry, itm)

    @staticmethod
    def show_items(qry):
        return connect(select_all, qry)

    @staticmethod
    def delete_item(qry):
        return connect(delete, qry)

    @staticmethod
    def update_item(qry):
        return connect(update, qry)

    @staticmethod
    def if_user_exists():
        sql = "SELECT count(*) as Total FROM users"
        result = connect(check_user_table, sql)
        if result is not None and result[0] == 0:
            return False
        else:
            return True
