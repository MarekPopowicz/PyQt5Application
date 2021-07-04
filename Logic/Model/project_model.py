class Project:

    def __init__(self,
                 p_id=0,
                 p_nr_sap='',
                 p_nr_psp='',
                 p_nr_sap_work_hours='',
                 p_project_priority=0,
                 p_task_type='',
                 p_main_device='',
                 p_place='',
                 p_street='',
                 p_engineer_name='',
                 p_registration_date='',
                 p_up_type='',
                 p_up_no='',
                 p_up_date='',
                 p_notice=''):
        self.id = p_id
        self.nr_sap = p_nr_sap
        self.nr_psp = p_nr_psp
        self.nr_sap_work_hours = p_nr_sap_work_hours
        self.project_priority = p_project_priority
        self.task_type = p_task_type
        self.main_device = p_main_device
        self.place = p_place
        self.street = p_street
        self.engineer_name = p_engineer_name
        self.registration_date = p_registration_date
        self.up_type = p_up_type
        self.up_no = p_up_no
        self.up_date = p_up_date
        self.notice = p_notice
