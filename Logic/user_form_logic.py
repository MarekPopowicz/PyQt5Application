import Data.db_query_commands as dbQry
from Data.db_manager import DBManager as DbMan
from Logic.Model.user_model import User
from Logic.tools import write_to_file, resource_path


class UserFormLogic:
    def __init__(self):
        self.user = User()
        self.get_current_user()

    def change_current_user(self, new_user):
        self.user.name = new_user[0]
        self.user.email = new_user[1]
        self.user.password = new_user[2]
        self.user.phone = new_user[3]

        if self.new_user() > 0:
            file = resource_path("Data\\") + "user_data.txt"
            user_data = f'{self.user.name}\n' \
                        f'{self.user.email}\n' \
                        f'{self.user.password}\n' \
                        f'{self.user.phone}\n'
            write_to_file(file, user_data, "a")
            return True
        else:
            return False

    def new_user(self):
        query = dbQry.QUERY_DROP_USER
        DbMan.delete_item(query)
        query = dbQry.QUERY_USER_SEQ_RESET
        DbMan.delete_item(query)
        query = dbQry.QUERY_INSERT_USER
        result = DbMan.add_new_items(query, (self.user.name,
                                             self.user.email,
                                             self.user.password,
                                             self.user.phone))
        return result

    def get_current_user(self):
        query = dbQry.QUERY_SELECT_USER
        result = DbMan.show_items(query)
        if result is not None and len(result) > 0:
            self.user.name = result[0][0]
            self.user.email = result[0][1]
            self.user.password = result[0][2]
            self.user.phone = result[0][3]
            return result
        else:
            return None
