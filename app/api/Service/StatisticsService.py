import os
from app.api.Service.DBService import DBService
from app.api.Service.DeptInfoService import DeptInfoService
from app.api.Service.HtmlService import HtmlService
from app.api.Service.PerformanceService import PerformanceService
from app.api.Factory.LogFactory import LogFactory
from Config import GLOBAL_CONFIG
from app.api.Service.XlsService import XlsService

logger = LogFactory().get_logger()


class StatisticsService(object):
    """Class StatisticsService"""

    def __init__(self):
        self._db_fields_info_service = DBService("DBFieldsInfo")

    def get_data_from_db(self, date_begin, date_end, mode):
        title_line, data, total_line= [], [], ["汇总", ""]
        performance_service = PerformanceService()
        dept_info_service = DeptInfoService()
        field_id_list, field_summable_list = [], []
        type_list = ["1", "1"]
        unsubmission_list = []
        fields_list, branch_list = [], []
        if mode == "daily":
            fields_list = self._db_fields_info_service.db_find_list_by_attribute_list_order_by(["business", "status"],
                                                                                               ["corporate", "1"],
                                                                                               "order_index")
            branch_list, unsubmission_list = performance_service.pre_check_submission(date_begin)
        elif mode == "range":
            fields_list = self._db_fields_info_service.db_find_list_by_attribute_list_order_by(
                ["business", "status", "statistics"], ["corporate", "1", "1"], "order_index")
            branch_list = dept_info_service.find_branch_kv_list("wangjing")
        elif mode == "detail":
            fields_list = self._db_fields_info_service.db_find_list_by_attribute_list_order_by(
                ["business", "status"],
                ["corporate", "1"],
                "order_index")
            branch_list = dept_info_service.find_branch_kv_list("wangjing")

        # 生成title
        title_line.append("序号")
        title_line.append("网点")
        if mode == "detail":
            title_line.append("日期")
            type_list.append("1")
            total_line.append("")
        elif mode == "range":
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
        if (mode == "detail") | (mode == "daily"):
            title_line.append("报送人")
        logger.info("Title行生成完毕。")

        # 生成data
        row = []
        line_num = 1
        if mode == "daily":
            # 简单汇总当日所有网点
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
            if mode == "range":
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
            elif mode == "detail":
                # 将某时间段内，每个网点业绩列出来
                for i, branch in enumerate(branch_list):
                    """第一层循环，以网点名称生成行"""
                    performance_list = performance_service.find_performance_by_range(date_begin, date_end, "dept_name",
                                                                                     branch["dept_name"])
                    if len(performance_list) > 0:
                        for k, performance in enumerate(performance_list):
                            row = [line_num, branch["dept_name"], performance.date.strftime("%Y-%m-%d")]
                            line_num += 1
                            extra_fields = performance.extra_fields
                            for j, a_f_id in enumerate(field_id_list):
                                """第二层循环，以可用字段生成列"""
                                if a_f_id in extra_fields:
                                    row.append(extra_fields[a_f_id])
                                    if a_f_id in field_summable_list:
                                        if extra_fields[a_f_id] != 0:
                                            if type_list[j + 3] == "int":
                                                total_line[j + 3] += int(extra_fields[a_f_id])
                                            elif type_list[j + 3] == "float":
                                                total_line[j + 3] += float(extra_fields[a_f_id])
                                    else:
                                        pass

                                else:
                                    row.append("")
                            row.append(performance.submit_user)
                            data.append(row)
                    else:
                        pass
                total_line.append("")
            logger.info("Total行生成完毕。")
        return title_line, data, total_line, type_list

    @staticmethod
    def create_files(date_begin, date_end, mode):
        try:
            title_line, data, total_line, type_list = StatisticsService().get_data_from_db(date_begin, date_end, mode)
            logger.info("统计数据Data构造成功")
            if mode == "daily":
                subject = "{} 网点报送汇总".format(date_begin)
                xls_file_name = os.path.join(GLOBAL_CONFIG.get_field("Excel", "xls_dir"), date_begin) + ".xls"
                html_file_name = os.path.join(GLOBAL_CONFIG.get_field("Html", "html_dir"), date_begin) + ".html"
            elif mode == "range":
                subject = "{} ~ {} 网点报送汇总".format(date_begin, date_end)
                xls_file_name = os.path.join(GLOBAL_CONFIG.get_field("Excel", "xls_dir"), "{} ~ {}_汇总".format(date_begin, date_end)) + ".xls"
                html_file_name = os.path.join(GLOBAL_CONFIG.get_field("Html", "html_dir"), "{} ~ {}_汇总".format(date_begin, date_end)) + ".html"
            else:
                subject = "{} ~ {} 网点报送明细".format(date_begin, date_end)
                xls_file_name = os.path.join(GLOBAL_CONFIG.get_field("Excel", "xls_dir"), "{} ~ {}_明细".format(date_begin, date_end)) + ".xls"
                html_file_name = os.path.join(GLOBAL_CONFIG.get_field("Html", "html_dir"), "{} ~ {}_明细".format(date_begin, date_end)) + ".html"
            style_list = HtmlService().get_style_list(mode)
            html_content = HtmlService().data_to_html(subject, title_line, data, total_line, style_list)
            HtmlService().html_2_file(html_content, html_file_name)
            logger.info("html内容构造成功")
            attachment_name = XlsService().data_to_xls(xls_file_name, title_line, data, total_line, type_list)
            logger.info("xls内容构造成功")
            return True
        except Exception as e:
            logger.error("Error: 内容构造失败:")
            logger.error(e)
            return False
