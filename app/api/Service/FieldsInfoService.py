import logging
import json

from app.api.Entity.FieldsInfo import FieldsInfo
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

    def find_available_fields_name(self):
        fields_list = self._db_fields_info_service.db_find_list_by_attribute_list_order_by(["business", "status"], ["corporate", "1"], "order_index")
        result = json.dumps(fields_list, default=DBFieldsInfo.obj_2_json_simple, sort_keys=False, ensure_ascii=False, indent=4)
        return result

    def update_field(self, field_id, request_json):
        old_fields = self._db_fields_info_service.db_find_one_by_attribute("field_id", field_id)
        setattr(old_fields, request_json["update_k"], request_json["update_v"])
        self._db_fields_info_service.db_update_db(old_fields)
        return True

    def create_field(self, request_json):
        field = self.fill_full_field(request_json)
        result = self._db_fields_info_service.db_save(field)
        if result:
            self._db_fields_info_service.db_commit()
            return True
        else:
            return False

    def sort_field(self, request_json):
        if isinstance(request_json, str):
            new_order = json.loads(request_json)
        else:
            new_order = request_json
        try:
            for item in new_order["new_order"]:
                field_id = item["id"]
                new = item["new_order"]
                field = self._db_fields_info_service.db_find_one_by_attribute("id", field_id)
                field.order_index = new
                result = self._db_fields_info_service.db_update(field, field_id)
                if result:
                    self._db_fields_info_service.db_commit()
        except Exception as e:
            logging.error(e)
            return False
        else:
            self._db_fields_info_service.db_commit()
        return True

    def check_exist(self, new_order):
        exist = None
        result = self._db_fields_info_service.db_find_column_by_attribute("new_order", new_order, id)
        if len(result) > 0:
            exist = result[0].id
        return exist

    def fill_full_field(self, json_raw):
        if isinstance(json_raw, str):
            json_obj = json.loads(json_raw)
        else:
            json_obj = json_raw
        max_id_field = self._db_fields_info_service.db_find_max_id()
        field_id = max_id_field.field_id.split('_')[0] + "_" + str(int(max_id_field.field_id.split('_')[1])+1)
        field_name = json_obj['field_name']
        field_type = json_obj['field_type']
        field_unit = json_obj['field_unit']
        max_order_field = self._db_fields_info_service.db_find_max_order()
        order_index = max_order_field.order_index + 1
        field = FieldsInfo(field_id, field_name, "corporate", field_type, field_unit, 1, order_index, 1)
        return field
