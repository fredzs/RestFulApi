import json

from app.api.ORM.DBFieldsInfo import DBFieldsInfo
from app.api.Service.DBService import DBService


class FieldsInfoService(object):
    """Class Performance"""
    def __init__(self):
        self._db_fields_info_service = DBService("DBFieldsInfo")

    def find_fields_list(self):
        fields_list = self._db_fields_info_service.db_find_list_by_attribute_order_by("business", "corporate", "order_index")
        result = json.dumps(fields_list, default=DBFieldsInfo.obj_2_json, sort_keys=False, ensure_ascii=False, indent=4)
        return result

    def find_fields_name(self):
        fields_list = self._db_fields_info_service.db_find_list_by_attribute_list_order_by(["business", "status"], ["corporate", "1"], "order_index")
        result = json.dumps(fields_list, default=DBFieldsInfo.obj_2_json_simple, sort_keys=False, ensure_ascii=False, indent=4)
        return result

    def update_field(self, request_json):
        old_fields = self._db_fields_info_service.db_find_one_by_attribute("field_id", request_json["field_id"])
        setattr(old_fields, request_json["update_k"], request_json["update_v"])
        self._db_fields_info_service.db_update_db(old_fields)
        return True
