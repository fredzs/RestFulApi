"""Class DeptInfo"""


class DeptInfo(object):
    """Class DeptInfo"""
    def __init__(self, dept_type, dept_name, corporate, dept_leader, dept_vice_1, dept_vice_2):
        self._dept_type = dept_type
        self._dept_name = dept_name
        self._corporate = corporate
        self._dept_leader = dept_leader
        self._dept_vice_1 = dept_vice_1
        self._dept_vice_2 = dept_vice_2

    def set_dept_type(self, dept_type):
        self._dept_type = dept_type

    def set_dept_name(self, dept_name):
        self._dept_name = dept_name

    def set_corporate(self, corporate):
        self._corporate = corporate

    def set_dept_leader(self, dept_leader):
        self._dept_leader = dept_leader

    def set_dept_vice_1(self, dept_vice_1):
        self._dept_vice_1 = dept_vice_1

    def set_dept_vice_2(self, dept_vice_2):
        self._dept_vice_2 = dept_vice_2

    @property
    def get_dept_type(self):
        return self._dept_type

    @property
    def get_dept_name(self):
        return self._dept_name

    @property
    def get_corporate(self):
        return self._corporate

    @property
    def get_dept_leader(self):
        return self._dept_leader

    @property
    def get_dept_vice_1(self):
        return self._dept_vice_1

    @property
    def get_dept_vice_2(self):
        return self._dept_vice_2

