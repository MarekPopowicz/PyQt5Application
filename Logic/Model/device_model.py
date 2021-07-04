class Device:
    def __init__(self,
                 d_id=0,
                 d_task_id=0,
                 d_device_type='',
                 d_device_width='',
                 d_device_long='',
                 d_regulation_type='',
                 d_notice=''):
        self.id = d_id
        self.task_id = d_task_id
        self.device_type = d_device_type
        self.device_width = d_device_width
        self.device_long = d_device_long
        self.regulation_type = d_regulation_type
        self.notice = d_notice
