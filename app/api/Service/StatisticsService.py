from app.api.Service.DBService import DBService
from app.api.Service.DeptInfoService import DeptInfoService
from app.api.Service.PerformanceService import PerformanceService
from app.api.Factory.LogFactory import LogFactory
from Config import GLOBAL_CONFIG

logger = LogFactory().get_logger()


class StatisticsService(object):
    """Class EmailService"""

    def __init__(self):
        self._db_fields_info_service = DBService("DBFieldsInfo")
        self._from_addr = ""
        self._password = ""
        self._to_addr = []
        self._smtp_server = ""

    def make_statistics(self, date_begin, date_end):
        title_line = []
        data = []
        total_line = ["汇总", ""]
        performance_service = PerformanceService()
        dept_info_service = DeptInfoService()
        field_id_list = []
        field_summable_list = []
        type_list = ["1", "1"]
        if date_begin == date_end:
            single_day = True
            fields_list = self._db_fields_info_service.db_find_list_by_attribute_list_order_by(["business", "status"],
                                                                                               ["corporate", "1"],
                                                                                               "order_index")
            branch_list = performance_service.pre_check_submission(date_begin)[0]
        else:
            single_day = False
            fields_list = self._db_fields_info_service.db_find_list_by_attribute_list_order_by(
                ["business", "status", "statistics"], ["corporate", "1", "1"], "order_index")
            branch_list = dept_info_service.find_branch_kv_list("wangjing")

        # 生成title
        title_line.append("序号")
        title_line.append("网点")
        for field in fields_list:
            type_list.append(field.field_type)
            if field.field_type == "int":
                title_line.append("%s(%s)" % (field.field_name, field.field_unit))
            elif field.field_type == "float":
                title_line.append("%s(%s)" % (field.field_name, field.field_unit))
            else:
                title_line.append("%s" % field.field_name)
            if field.statistics == 1:
                field_summable_list.append(field.field_id)
                total_line.append(0)
            else:
                total_line.append("")
            field_id_list.append(field.field_id)
        if single_day:
            title_line.append("报送人")
        # 生成data
        for i, branch in enumerate(branch_list):
            """第一层循环，以网点名称生成行"""
            if single_day:
                performance_list = performance_service.find_performance_by_date(date_begin, "dept_name", branch["dept_name"])
                if len(performance_list) == 1:
                    row = [i + 1, branch["dept_name"]]
                    performance = performance_list[0]
                    extra_fields = performance.extra_fields
                    for j, a_f_id in enumerate(field_id_list):
                        """第二层循环，以可用字段生成列"""
                        if a_f_id in extra_fields:
                            row.append(extra_fields[a_f_id])
                            if a_f_id in field_summable_list:
                                if extra_fields[a_f_id] != 0:
                                    if type_list[j + 2] == "int":
                                        total_line[j + 2] += int(extra_fields[a_f_id])
                                    elif type_list[j + 2] == "float":
                                        total_line[j + 2] += float(extra_fields[a_f_id])
                            else:
                                pass
                        else:
                            row.append("")
                    row.append(branch["submit_user"])
                    type_list.append("1")
                else:
                    continue
            else:
                performance_list = performance_service.find_performance_by_range(date_begin, date_end, "dept_name", branch["dept_name"])
                if len(performance_list) > 0:
                    temp_list = [0 for x in range(0, len(field_summable_list))]
                    row = [i + 1, branch["dept_name"]]
                    for k, performance in enumerate(performance_list):
                        extra_fields = performance.extra_fields
                        for j, a_f_id in enumerate(field_id_list):
                            """第二层循环，以可用字段生成列"""
                            if a_f_id in extra_fields:
                                if a_f_id in field_summable_list:
                                    if extra_fields[a_f_id] != 0:
                                        if type_list[j + 2] == "int":
                                            temp_list[j] += int(extra_fields[a_f_id])
                                            total_line[j + 2] += int(extra_fields[a_f_id])
                                        elif type_list[j + 2] == "float":
                                            temp_list[j] += float(extra_fields[a_f_id])
                                            total_line[j + 2] += float(extra_fields[a_f_id])
                                else:
                                    pass
                            else:
                                pass
                                # row.append("" for x in range(0, len(field_summable_list)))
                    row.extend(temp_list)
                else:
                    row.extend([])
            data.append(row)
        total_line.append("")
        return title_line, data, total_line, type_list
