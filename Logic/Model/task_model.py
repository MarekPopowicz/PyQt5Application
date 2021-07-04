class Task:

    def __init__(self,
                 t_id=0,
                 t_project_id=0,
                 t_register_no='',
                 t_sheet_no='',
                 t_parcel_no='',
                 t_area_name='',
                 t_owner_data='',
                 t_notice=''):

        self.id = t_id
        self.project_id = t_project_id
        self.register_no = t_register_no
        self.parcel_no = t_parcel_no
        self.sheet_no = t_sheet_no
        self.area_name = t_area_name
        self.owner_data = t_owner_data
        self.notice = t_notice
