import xlrd, xlwt
from Const import *
from app.api.Factory.LogFactory import LogFactory

logger = LogFactory().get_logger()


class XlsService(object):
    """Class XlsService"""
    @staticmethod
    def data_to_xls(file_name, title_line, data, total_line, type_list, mode):
        xls_file = xlwt.Workbook(style_compression=2)
        sheet = xls_file.add_sheet("业绩", cell_overwrite_ok=True)
        current_row_number = 0
        width_list, style_list = XlsService().get_style_list(mode)

        # 生成首行
        title_style = xlwt.easyxf('font:height 200, bold on;align: wrap on, vert centre, horiz center;')

        for i, title_cell in enumerate(title_line):
            sheet.write(current_row_number, i, title_cell, title_style)
        current_row_number += 1
        for i, width in enumerate(width_list):
            sheet.col(i).width = width

        # 生成数据行
        for i, row in enumerate(data):
            for j, col in enumerate(row):
                style_str = style_list[j]
                data_style = xlwt.easyxf(style_str)
                if col != "":
                    if type_list[j] == "int":
                        sheet.write(current_row_number, j, int(col), data_style)
                    elif type_list[j] == "float":
                        sheet.write(current_row_number, j, float(col), data_style)
                    else:
                        sheet.write(current_row_number, j, col, data_style)
                else:
                    sheet.write(current_row_number, j, col, data_style)
            current_row_number += 1

        # 生成汇总行
        total_style = xlwt.easyxf('font:height 200, bold on;align: wrap on, vert centre, horiz center;')
        for i, total_cell in enumerate(total_line):
            sheet.write(current_row_number, i, total_cell, total_style)

        xls_file.save(file_name)
        return file_name

    @staticmethod
    def get_style_list(mode):
        if mode == "detail":
            return XLS_WIDTH_LIST_DETAIL, XLS_STYLE_LIST_DETAIL
        if mode == "range":
            return XLS_WIDTH_LIST_RANGE, XLS_STYLE_LIST_RANGE
        if mode == "daily":
            return XLS_WIDTH_LIST_DAILY, XLS_STYLE_LIST_DAILY
