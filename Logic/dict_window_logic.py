import Data.db_query_commands as dbQry
from Data.db_manager import DBManager as DbMan
import Gui.Components.constants as Const


class DictionaryWindowLogic:
    def __init__(self, dictionary_name):
        self.name = dictionary_name

    def get_dictionary_items(self):
        sql_query_str = ''
        if self.name == Const.TASKS:
            sql_query_str = dbQry.QUERY_SELECT_ALL_TASK_TYPES
        elif self.name == Const.STREETS:
            sql_query_str = dbQry.QUERY_SELECT_ALL_STREETS
        elif self.name == Const.PLACES:
            sql_query_str = dbQry.QUERY_SELECT_ALL_PLACES
        elif self.name == Const.DEVICES:
            sql_query_str = dbQry.QUERY_SELECT_ALL_DEVICE_TYPES
        elif self.name == Const.DOCUMENTS:
            sql_query_str = dbQry.QUERY_SELECT_ALL_DOCUMENTS
        result = DbMan.show_items(sql_query_str)
        return result

    def delete_item(self, item):
        sql_query_str = ''
        if self.name == Const.TASKS:
            sql_query_str = dbQry.QUERY_DELETE_TASK_TYPE
        elif self.name == Const.STREETS:
            sql_query_str = dbQry.QUERY_DELETE_STREET
        elif self.name == Const.PLACES:
            sql_query_str = dbQry.QUERY_DELETE_PLACE
        elif self.name == Const.DEVICES:
            sql_query_str = dbQry.QUERY_DELETE_DEVICE_TYPE
        elif self.name == Const.DOCUMENTS:
            sql_query_str = dbQry.QUERY_DELETE_DOCUMENT

        query = sql_query_str.replace('?', item)
        result = DbMan.delete_item(query)
        return result

    def add_item(self, item):
        sql_query_str = ''
        if self.name == Const.TASKS:
            sql_query_str = dbQry.QUERY_INSERT_TASK_TYPE
        elif self.name == Const.STREETS:
            sql_query_str = dbQry.QUERY_INSERT_STREET
        elif self.name == Const.PLACES:
            sql_query_str = dbQry.QUERY_INSERT_PLACE
        elif self.name == Const.DEVICES:
            sql_query_str = dbQry.QUERY_INSERT_DEVICE_TYPE
        elif self.name == Const.DOCUMENTS:
            sql_query_str = dbQry.QUERY_INSERT_DOCUMENT

        result = DbMan.add_new_item(sql_query_str, item)
        return result

    def update_item(self, old_item, new_item):
        sql_query_str = ''
        if self.name == Const.TASKS:
            sql_query_str = dbQry.QUERY_UPDATE_TASK_TYPE
        elif self.name == Const.STREETS:
            sql_query_str = dbQry.QUERY_UPDATE_STREET
        elif self.name == Const.PLACES:
            sql_query_str = dbQry.QUERY_UPDATE_PLACE
        elif self.name == Const.DEVICES:
            sql_query_str = dbQry.QUERY_UPDATE_DEVICE_TYPE
        elif self.name == Const.DOCUMENTS:
            sql_query_str = dbQry.QUERY_UPDATE_DOCUMENT

        sql_query_str = sql_query_str.replace('§', new_item)
        query = sql_query_str.replace('?', old_item)
        result = DbMan.update_item(query)
        return result
