"""Class FieldsInfo"""


class FieldsInfo(object):
    """Class FieldsInfo"""
    def __init__(self, field_name, field_type, status):
        self._field_name = field_name
        self._field_type = field_type
        self._status = status

    def set_field_name(self, field_name):
        self._field_name = field_name

    def set_field_type(self, field_type):
        self._field_type = field_type

    def set_status(self, status):
        self._status = status

    @property
    def get_field_name(self):
        return self._field_name

    @property
    def get_field_type(self):
        return self._field_type

    @property
    def get_status(self):
        return self._status
