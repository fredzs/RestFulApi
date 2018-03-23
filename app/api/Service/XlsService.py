import xlrd, xlwt
from Const import *
from app.api.Factory.LogFactory import LogFactory

logger = LogFactory().get_logger()


class XlsService(object):
    """Class XlsService"""
    @staticmethod
    def data_to_xls(file_name, title_line, data, total_line, type_list, xls_style_list):
        xls_file = xlwt.Workbook()
        sheet = xls_file.add_sheet("业绩", cell_overwrite_ok=True)
        current_row_number = 0

        # 生成首行
        alignment = xlwt.Alignment()
        # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
        alignment.vert = xlwt.Alignment.VERT_CENTER
        title_style = xlwt.XFStyle()
        title_style.alignment = alignment

        for i, title_cell in enumerate(title_line):
            sheet.write(current_row_number, i, title_cell, title_style)
        current_row_number += 1
        sheet.row(0).height = 64

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

    @staticmethod
    def get_style_list(mode):
        if mode == "detail":
            return XLS_STYLE_LIST_DETAIL
        if mode == "range":
            return XLS_STYLE_LIST_RANGE
        if mode == "daily":
            return XLS_STYLE_LIST_DAILY
