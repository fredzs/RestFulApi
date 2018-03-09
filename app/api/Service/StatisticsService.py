import xlrd, xlwt
from app.api.Service.DBService import DBService
from app.api.Service.DeptInfoService import DeptInfoService
from app.api.Service.PerformanceService import PerformanceService
from app.api.Factory.LogFactory import LogFactory

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
        unsubmission_list = []
        if date_begin == date_end:
            single_day = True
            fields_list = self._db_fields_info_service.db_find_list_by_attribute_list_order_by(["business", "status"],
                                                                                               ["corporate", "1"],
                                                                                               "order_index")
            branch_list, unsubmission_list = performance_service.pre_check_submission(date_begin)
        else:
            single_day = False
            fields_list = self._db_fields_info_service.db_find_list_by_attribute_list_order_by(
                ["business", "status", "statistics"], ["corporate", "1", "1"], "order_index")
            branch_list = dept_info_service.find_branch_kv_list("wangjing")

        # 生成title
        title_line.append("序号")
        title_line.append("网点")
        if not single_day:
            title_line.append("报送天数")
            type_list.append("1")
            total_line.append("")
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
        row = []
        if single_day:
            # 简单汇总当日所有网点
            line_num = 1
            for i, branch in enumerate(branch_list):
                """第一层循环，以网点名称生成行"""
                performance_list = performance_service.find_performance_by_date(date_begin, "dept_name",
                                                                                branch["dept_name"])
                if len(performance_list) == 1:
                    row = [i + 1, branch["dept_name"]]
                    line_num += 1
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
                    pass
                data.append(row)
            for i, branch in enumerate(unsubmission_list):
                row = [i + line_num, branch["dept_name"]]
                temp_row = ["" for x in range(0, len(field_id_list))]
                temp_row.append("")
                row.extend(temp_row)
                data.append(row)
            total_line.append("")
        else:
            # 将某时间段内，每个网点业绩求和汇总
            for i, branch in enumerate(branch_list):
                """第一层循环，以网点名称生成行"""
                performance_list = performance_service.find_performance_by_range(date_begin, date_end, "dept_name",
                                                                                 branch["dept_name"])
                row = [i + 1, branch["dept_name"], len(performance_list)]
                if len(performance_list) > 0:
                    temp_list = [0 for x in range(0, len(field_summable_list))]
                    for k, performance in enumerate(performance_list):
                        extra_fields = performance.extra_fields
                        for j, a_f_id in enumerate(field_id_list):
                            """第二层循环，以可用字段生成列"""
                            if a_f_id in extra_fields:
                                if a_f_id in field_summable_list:
                                    if extra_fields[a_f_id] != 0:
                                        if type_list[j + 3] == "int":
                                            temp_list[j] += int(extra_fields[a_f_id])
                                            total_line[j + 3] += int(extra_fields[a_f_id])
                                        elif type_list[j + 3] == "float":
                                            temp_list[j] += float(extra_fields[a_f_id])
                                            total_line[j + 3] += float(extra_fields[a_f_id])
                                else:
                                    pass
                            else:
                                pass
                                # row.append("" for x in range(0, len(field_summable_list)))
                    row.extend(temp_list)
                else:
                    temp_list = ["" for x in range(0, len(field_summable_list))]
                    row.extend(temp_list)
                data.append(row)
        return title_line, data, total_line, type_list

    @staticmethod
    def html_2_file(html, file_name):
        with open(file_name, 'w') as f:
            f.write(html)

    @staticmethod
    def data_to_html(subject, title_line, data, total_line):
        content = "<html>"
        content += "<head><style>tr{font-size:12px;text-align:center;}td{font-size:12px;text-align:center;width:40px;}.td1{width:90px;}.td5{width:80px;}.td15{width:50px;}</style></head>"

        content += "<body><h2>{}</h2>".format(subject)
        content += "<table border=\"1\" style= \"border-collapse: collapse; border-color: #BCD1E6;\"><tbody><tr style= \"border-color: #9AA2A9;\">"

        # 生成首行
        for i, title_td in enumerate(title_line):
            if (i == 1) | (i == 5) | (i == len(title_line) - 1):
                content += "<td class=\"td{}\"><p><B>{}</B></p></td>".format(i, title_td)
            else:
                content += "<td><p><B>{}</B></p></td>".format(title_td)
            content += ""
        content += "</tr>"
        # 生成数据行
        for i, row in enumerate(data):
            """第一层循环，以网点名称生成行"""
            content += "<tr>"
            for col in row:
                """第二层循环，以可用字段生成列"""
                if col == "":
                    content += "<td >-</td>"
                else:
                    content += "<td >{}</td>".format(col)
            content += "</tr>"
        # 生成汇总行
        content += "<tr>"
        for total_td in total_line:
            content += "<td ><p><B>{}</B></p></td>".format(total_td)
        content += "</tr>"
        content += "</tbody></table>"
        content += "</body></html>"
        return content

    @staticmethod
    def data_to_xls(file_name, title_line, data, total_line, type_list):
        xls_file = xlwt.Workbook()
        sheet = xls_file.add_sheet("业绩", cell_overwrite_ok=True)
        current_row_number = 0
        # 生成首行
        for i, title_cell in enumerate(title_line):
            sheet.write(current_row_number, i, title_cell)
        current_row_number += 1

        # 生成数据行
        for i, row in enumerate(data):
            for j, col in enumerate(row):
                if col != "":
                    if type_list[j] == "int":
                        sheet.write(current_row_number, j, int(col))
                    elif type_list[j] == "float":
                        sheet.write(current_row_number, j, float(col))
                    else:
                        sheet.write(current_row_number, j, col)
                else:
                    sheet.write(current_row_number, j, col)
            current_row_number += 1

        # 生成汇总行
        for i, total_cell in enumerate(total_line):
            sheet.write(current_row_number, i, total_cell)

        xls_file.save(file_name)
        return file_name
