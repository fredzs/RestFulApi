"""Class DeptInfo"""


class UserInfo(object):
    """Class DeptInfo"""
    def __init__(self, user_name, wx_nick_name, dept_id, role):
        self._user_name = user_name
        self._wx_nick_name = wx_nick_name
        self._dept_id = dept_id
        self._role = role

    def set_user_name(self, user_name):
        self._user_name = user_name

    def set_wx_nick_name(self, wx_nick_name):
        self._wx_nick_name = wx_nick_name

    def set_dept_id(self, dept_id):
        self._dept_id = dept_id

    def set_role(self, role):
        self._role = role

    @property
    def get_user_name(self):
        return self._user_name

    @property
    def get_wx_nick_name(self):
        return self._wx_nick_name

    @property
    def get_dept_id(self):
        return self._dept_id

    @property
    def get_role(self):
        return self._role
