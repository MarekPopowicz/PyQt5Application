import os
import sqlite3
import sys
from sqlite3 import Error

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog

from Gui.Components.constants import resource_path
from Gui.Components.msg_dialogs import MsgBox
import Gui.Components.constants as Const


def write_to_file(path_file_name, data_to_write, mode):
    """ write document to file """
    try:
        with open(path_file_name, mode=mode, encoding='utf8') as file:
            file.write(data_to_write)
    except OSError:
        return False

    return True


def read_doc_lines(path_file_name):
    """ Return list of file document's paragraphs """
    doc_line_list = []
    try:
        with open(path_file_name) as file:
            doc = file.readlines()
            for line in doc:
                doc_line_list.append(line.rstrip('\n'))
    except OSError:
        pass

    return doc_line_list


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
        text = ''

        data_path = resource_path("Data\\")
        file = data_path + "user_data.txt"
        data = read_doc_lines(file)

        # Plik danych zawiera informacje
        if len(data) != 0:
            path_db = data[0].rstrip('\n')

            # Brak pliku w podanej lokalizacji
            if not os.path.exists(path_db):
                answer = MsgBox('ok_cancel_dlg', 'Pytanie', 'Baza danych została usunięta lub przeniesiona.\n'
                                                            'Czy utworzyć nową bazę danych ?',
                                QIcon(Const.APP_ICON)).last_user_answer
                if answer:
                    filename, _ = QFileDialog.getSaveFileName(None, "Wybierz lokalizację dla pliku nowej bazy danych.",
                                                              os.path.expanduser("~/Desktop/database.db"),
                                                              "DataBase (*.db)")
                    open(file, "w").close()
                    write_to_file(file, filename + '\n', "w")

                else:
                    filename, _ = QFileDialog.getOpenFileName(None, "Wskaż lokalizację dotychczasowej bazy danych.",
                                                              os.path.expanduser("~/Desktop/database.db"),
                                                              "DataBase (*.db)")
                    if filename == '':
                        open(file, "w").close()
                        sys.exit()

                    db_path = read_doc_lines(file)
                    db_path[0] = filename
                    for item in db_path:
                        text = text + item + '\n'
                        write_to_file(file, text, "w")

                connection = create_connection(filename)
            # Istnieje plik w podanej lokalizacji
            else:
                connection = create_connection(path_db)

        # Plik danych nie zawiera informacji
        else:
            answer = MsgBox('ok_cancel_dlg', 'Pytanie', 'Dalsze korzystanie z aplikacji wymaga\nutworzenia bazy '
                                                        'danych.\n\n'
                                                        'Czy utworzyć nową bazę danych ?',
                            QIcon(Const.APP_ICON)).last_user_answer
            if answer:
                filename, _ = QFileDialog.getSaveFileName(None, "Wybierz lokalizację nowej bazy danych.",
                                                          os.path.expanduser("~/Desktop/database.db"),
                                                          "DataBase (*.db)")
                if filename == '':
                    open(file, "w").close()
                    sys.exit()

                write_to_file(file, filename + '\n', "w")
                connection = create_connection(filename)
            else:
                sys.exit()

        return connection


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
