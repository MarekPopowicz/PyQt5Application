# region TABLE CREATION
# Users
SQL_CREATE_USERS_TABLE = """ CREATE TABLE IF NOT EXISTS users (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        name NVARCHAR(80) NOT NULL,
                                        email NVARCHAR(80) NOT NULL,
                                        password NVARCHAR(20),
                                        phone NVARCHAR(20)
                                    ); """
# Project
SQL_CREATE_PROJECTS_TABLE = """ CREATE TABLE IF NOT EXISTS projects (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        nr_sap NVARCHAR(20) NOT NULL,
                                        nr_psp NVARCHAR(10) NOT NULL,
                                        nr_sap_work_hours NVARCHAR(10) NOT NULL,
                                        project_priority INTEGER DEFAULT 0, 
                                        task_type NVARCHAR(50) NOT NULL,
                                        task_name NVARCHAR(255) NOT NULL,
                                        place NVARCHAR(255) NOT NULL,
                                        street NVARCHAR(255),
                                        engineer_name NVARCHAR(80) NOT NULL,
                                        registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                        up_type NVARCHAR(100) NOT NULL,
                                        up_no NVARCHAR(100) NOT NULL,
                                        notice TEXT
                                    ); """
# Tasks
SQL_CREATE_TASKS_TABLE = """CREATE TABLE IF NOT EXISTS tasks (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    project_id INTEGER NOT NULL,
                                    register_no NVARCHAR(25) NOT NULL,
                                    parcel_no NVARCHAR(5) NOT NULL,
                                    map_sheet_no NVARCHAR(5) NOT NULL,
                                    area_name NVARCHAR(50) NOT NULL,
                                    owner_data TEXT NOT NULL,
                                    notice TEXT,
                                    FOREIGN KEY (project_id) REFERENCES projects (id)
                                );"""
# Attachments
SQL_CREATE_ATTACHMENTS_TABLE = """CREATE TABLE IF NOT EXISTS attachments (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    project_id INTEGER NOT NULL,
                                    document_name NVARCHAR(255),
                                    document_original INTEGER DEFAULT 0,
                                    document_count INTEGER DEFAULT 1,
                                    notice TEXT,
                                    FOREIGN KEY (project_id) REFERENCES projects (id)
                                );"""
# Devices
SQL_CREATE_DEVICE_TABLE = """CREATE TABLE IF NOT EXISTS devices (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    task_id INTEGER NOT NULL,
                                    device_type NVARCHAR(80) NOT NULL,
                                    device_width REAL NOT NULL,
                                    device_long REAL NOT NULL,
                                    regulation_type NVARCHAR(255) NOT NULL,
                                    notice TEXT,
                                    FOREIGN KEY (task_id) REFERENCES tasks (id)
                                );"""

# Dictionaries
# Tasks
SQL_CREATE_PROJECTS_TASKS_TYPES = """ CREATE TABLE IF NOT EXISTS dict_tasks_names (
                                        task_name NVARCHAR(255) UNIQUE
                                    ); """
# Notary Offices
SQL_CREATE_NOTARY_OFFICES = """ CREATE TABLE IF NOT EXISTS dict_notary_offices (
                                        notary_office NVARCHAR(255) UNIQUE
                                    ); """
# Streets
SQL_CREATE_STREETS = """ CREATE TABLE IF NOT EXISTS dict_streets_names (
                                        street_name NVARCHAR(100) UNIQUE
                                    ); """
# Places
SQL_CREATE_PLACES = """ CREATE TABLE IF NOT EXISTS dict_places_names (
                                        place_name NVARCHAR(255) UNIQUE
                                    ); """
# Documents
SQL_CREATE_DOCUMENTS = """ CREATE TABLE IF NOT EXISTS dict_documents_names (
                                        document_name NVARCHAR(255) UNIQUE
                                    ); """
# Regulations
SQL_CREATE_REGULATIONS = """ CREATE TABLE IF NOT EXISTS dict_regulations (
                                        regulation NVARCHAR(255) UNIQUE
                                    ); """
# Devices
SQL_CREATE_DEVICE_TYPES = """ CREATE TABLE IF NOT EXISTS dict_devices_types (
                                        device_type NVARCHAR(255) UNIQUE
                                    ); """
# endregion

# region DATA OPERATION QUERIES
# Insert
QUERY_INSERT_PROJECT = 'INSERT INTO projects(' \
                       'nr_sap, ' \
                       'nr_psp, ' \
                       'nr_sap_work_hours, ' \
                       'project_priority, ' \
                       'task_type, ' \
                       'task_name, ' \
                       'place, ' \
                       'street, ' \
                       'engineer_name, ' \
                       'up_type, ' \
                       'up_no, ' \
                       'notice) ' \
                       'VALUES(?,?,?,?,?,?,?,?,?,?,?,?);'

QUERY_INSERT_TASK = 'INSERT INTO tasks(project_id, register_no, parcel_no, map_sheet_no, area_name, owner_data, ' \
                    'notice) VALUES(?,?,?,?,?,?,?);'

QUERY_INSERT_DEVICE = 'INSERT INTO devices(task_id, device_type, device_long, device_width, regulation_type, ' \
                      'notice) VALUES(?,?,?,?,?,?);'

QUERY_INSERT_ATTACHMENT = 'INSERT INTO attachments(project_id, document_name, ' \
                          'document_original, document_count, notice) VALUES(?,?,?,?,?);'

QUERY_INSERT_USER = 'INSERT INTO users(name, email, password, phone) VALUES(?,?,?,?);'

QUERY_INSERT_TASK_TYPE = 'INSERT OR IGNORE INTO dict_tasks_names VALUES (?);'
QUERY_INSERT_NOTARY_OFFICE = 'INSERT OR IGNORE INTO dict_notary_offices VALUES (?);'
QUERY_INSERT_STREET = 'INSERT OR IGNORE INTO dict_streets_names VALUES(?);'
QUERY_INSERT_PLACE = 'INSERT OR IGNORE INTO dict_places_names VALUES(?);'
QUERY_INSERT_DOCUMENT = 'INSERT OR IGNORE INTO dict_documents_names VALUES(?);'
QUERY_INSERT_REGULATION = 'INSERT OR IGNORE INTO dict_regulations VALUES(?);'
QUERY_INSERT_DEVICE_TYPE = 'INSERT OR IGNORE INTO dict_devices_types VALUES(?);'

# Delete
QUERY_DELETE_TASK_TYPE = 'DELETE FROM dict_tasks_names WHERE task_name LIKE "%?%";'
QUERY_DELETE_NOTARY_OFFICE = 'DELETE FROM dict_notary_offices WHERE notary_office LIKE "%?%";'
QUERY_DELETE_STREET = 'DELETE FROM dict_streets_names WHERE street_name LIKE "%?%";'
QUERY_DELETE_PLACE = 'DELETE FROM dict_places_names WHERE place_name LIKE "%?%";'
QUERY_DELETE_DOCUMENT = 'DELETE FROM dict_documents_names WHERE document_name LIKE "%?%";'
QUERY_DELETE_REGULATION = 'DELETE FROM dict_regulations WHERE regulation LIKE "%?%";'
QUERY_DELETE_DEVICE_TYPE = 'DELETE FROM dict_devices_types WHERE device_type LIKE "%?%";'

QUERY_DELETE_PROJECT = 'DELETE FROM projects WHERE id = ?;'
QUERY_DELETE_TASK = 'DELETE FROM tasks WHERE id = ?;'
QUERY_DELETE_DEVICE = 'DELETE FROM devices WHERE id = ?;'
QUERY_DELETE_ATTACHMENT = 'DELETE FROM attachments WHERE id = ?;'
QUERY_DELETE_USER = 'DELETE FROM users WHERE id = ?;'
QUERY_DROP_USER = 'DELETE FROM users;'
QUERY_USER_SEQ_RESET = 'DELETE FROM sqlite_sequence WHERE name = "users";'

# Update
QUERY_UPDATE_TASK_TYPE = 'UPDATE dict_tasks_names SET task_name = "§" WHERE task_name LIKE "%?%";'
QUERY_UPDATE_NOTARY_OFFICE = 'UPDATE dict_notary_offices SET notary_office = "§" WHERE notary_office LIKE "%?%";'
QUERY_UPDATE_STREET = 'UPDATE dict_streets_names SET street_name = "§" WHERE street_name LIKE "%?%";'
QUERY_UPDATE_PLACE = 'UPDATE dict_places_names SET place_name = "§" WHERE place_name LIKE "%?%";'
QUERY_UPDATE_DOCUMENT = 'UPDATE dict_documents_names SET document_name = "§" WHERE document_name LIKE "%?%";'
QUERY_UPDATE_REGULATION = 'UPDATE dict_regulations SET regulation = "§" WHERE regulation LIKE "%?%";'
QUERY_UPDATE_DEVICE_TYPE = 'UPDATE dict_devices_types SET device_type = "§" WHERE device_type LIKE "%?%";'

QUERY_UPDATE_TASK = 'UPDATE tasks SET register_no = "register_no_value", parcel_no = "parcel_no_value", ' \
                    'map_sheet_no = "map_sheet_no_value", area_name = "area_name_value", ' \
                    'owner_data = "owner_data_value", notice = "notice_value" WHERE id = id_value;'

QUERY_UPDATE_PROJECT = 'UPDATE projects SET nr_sap = "nr_sap_value", nr_psp = "nr_psp_value", nr_sap_work_hours = ' \
                       '"nr_sap_work_hours_value", project_priority = project_priority_value, ' \
                       'task_type = "task_type_value", task_name = "task_name_value", place = "place_value", street = ' \
                       '"street_value", up_type = "up_type_value", up_no = "up_no_value", ' \
                       'notice = "notice_value"  WHERE id = id_value;'

QUERY_UPDATE_DEVICE = 'UPDATE devices SET device_type = ?, device_width = ?, device_long = ?, regulation_type = ?, ' \
                      'notice = ? WHERE id = ?; '
QUERY_UPDATE_ATTACHMENT = 'UPDATE attachments SET document_name = ?, document_original = ?, ' \
                          'document_count = ?, notice = ? WHERE id = ?; '

# Select
QUERY_SELECT_TASKS = 'SELECT id, register_no, parcel_no, map_sheet_no, area_name, owner_data, notice FROM tasks ' \
                    'WHERE project_id = ?;'
QUERY_SELECT_TASK = 'SELECT id, register_no, parcel_no, map_sheet_no, area_name, owner_data, notice FROM tasks ' \
                    'WHERE id = ?;'

QUERY_SELECT_PROJECT = 'SELECT nr_sap, nr_psp, nr_sap_work_hours, project_priority, task_name, task_type, place, ' \
                       'street, engineer_name, registration_date, up_type, up_no, notice FROM projects WHERE id = ?;'
QUERY_SELECT_ALL_PROJECTS = 'SELECT id, nr_sap, nr_psp, nr_sap_work_hours, project_priority, task_name, task_type, ' \
                            'place, street, engineer_name, registration_date, up_type, up_no, notice FROM projects; '
QUERY_SELECT_DEVICE = 'SELECT id, task_id, device_type, device_width, device_long, regulation_type, notice FROM ' \
                      'devices WHERE id = ?; '

QUERY_SELECT_DEVICES = 'SELECT id, device_type, device_long, device_width, regulation_type, notice FROM ' \
                            'devices WHERE task_id = ?; '

QUERY_SELECT_ATTACHMENT = 'SELECT id, project_id, document_name FROM attachments WHERE id = ?; '
QUERY_SELECT_ATTACHMENTS = 'SELECT id, project_id, document_name FROM attachments WHERE project_id = ?; '
QUERY_SELECT_USER = 'SELECT name, email, password, phone FROM users;'

QUERY_SELECT_ALL_TASK_TYPES = 'SELECT task_name FROM dict_tasks_names ORDER BY task_name ASC;'
QUERY_SELECT_ALL_NOTARY_OFFICES = 'SELECT notary_office FROM dict_notary_offices ORDER BY notary_office ASC;'
QUERY_SELECT_ALL_STREETS = 'SELECT street_name FROM dict_streets_names ORDER BY street_name ASC;'
QUERY_SELECT_ALL_PLACES = 'SELECT place_name FROM dict_places_names ORDER BY place_name ASC;'
QUERY_SELECT_ALL_DOCUMENTS = 'SELECT document_name FROM dict_documents_names ORDER BY document_name ASC;'
QUERY_SELECT_ALL_REGULATIONS = 'SELECT regulation FROM dict_regulations ORDER BY regulation ASC;'
QUERY_SELECT_ALL_DEVICE_TYPES = 'SELECT device_type FROM dict_devices_types ORDER BY device_type ASC;'

QUERY_SELECT_TASK_TYPE = 'SELECT task_name FROM dict_tasks_names WHERE task_name LIKE "%?%";'
QUERY_SELECT_NOTARY_OFFICE = 'SELECT notary_office FROM dict_notary_offices WHERE notary_office LIKE "%?%";'
QUERY_SELECT_STREET = 'SELECT street_name FROM dict_streets_names WHERE street_name LIKE "%?%";'
QUERY_SELECT_PLACE = 'SELECT place_name FROM dict_places_names WHERE place_name LIKE "%?%";'
QUERY_SELECT_DOCUMENT = 'SELECT document_name FROM dict_documents_names WHERE document_name LIKE "%?%";'
QUERY_SELECT_DEVICE_TYPE = 'SELECT device_type FROM dict_devices_types WHERE device_type LIKE "%?%";'
# endregion
