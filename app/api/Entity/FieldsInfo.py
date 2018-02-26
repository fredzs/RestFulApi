"""Class FieldsInfo"""


class FieldsInfo(object):
    """Class FieldsInfo"""
    def __init__(self, field_id, field_name, business, field_type, field_unit, order_index, status):
        self._field_id = field_id
        self._field_name = field_name
        self._business = business
        self._field_type = field_type
        self._field_unit = field_unit
        self._order_index = order_index
        self._status = status

    def set_field_id(self, field_id):
        self._field_id = field_id

    def set_field_name(self, field_name):
        self._field_name = field_name

    def set_business(self, business):
        self._business = business

    def set_field_type(self, field_type):
        self._field_type = field_type

    def set_field_unit(self, field_unit):
        self._field_unit = field_unit

    def set_order_index(self, order_index):
        self._order_index = order_index

    def set_status(self, status):
        self._status = status

    @property
    def get_field_id(self):
        return self._field_id

    @property
    def get_field_name(self):
        return self._field_name

    @property
    def get_business(self):
        return self._business

    @property
    def get_field_type(self):
        return self._field_type

    @property
    def get_field_unit(self):
        return self._field_unit

    @property
    def get_order_index(self):
        return self._order_index

    @property
    def get_status(self):
        return self._status
