from app.api.Factory.LogFactory import LogFactory
from Const import *
logger = LogFactory().get_logger()


class HtmlService(object):
    """Class HtmlService"""
    @staticmethod
    def html_2_file(html, file_name):
        with open(file_name, 'w') as f:
            f.write(html)

    @staticmethod
    def data_to_html(subject, title_line, data, total_line, style_list):
        if style_list is None:
            style_list = ["width:30px;", "width:90px;", "width:80px;", "", "", "", "width:80px;", "", "", "", "", "", "", "", "", "", "width:50px;"]
        content = "<html>"
        content += "<head><style>tr{font-size:12px;text-align:center;}td{font-size:12px;text-align:center;width:40px;}.td1{width:90px;}.td2{width:80px;}.td3{width:50px;}</style></head>"

        content += "<body><h2>{}</h2>".format(subject)
        content += "<table border=\"1\" style= \"border-collapse: collapse; border-color: #BCD1E6;\"><tbody><tr style= \"border-color: #9AA2A9;\">"

        # 生成首行
        for i, title_td in enumerate(title_line):
            content += "<td style=\"{}\"><p><B>{}</B></p></td>".format(style_list[i], title_td)
            content += ""
        content += "</tr>"
        logger.info("Table_Title行生成完毕。")
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
        logger.info("Table_中间行生成完毕。")
        # 生成汇总行
        content += "<tr>"
        for total_td in total_line:
            content += "<td ><p><B>{}</B></p></td>".format(total_td)
        content += "</tr>"
        logger.info("Table_Total行生成完毕。")
        content += "</tbody></table>"
        content += "</body></html>"
        return content

    @staticmethod
    def get_style_list(mode):
        if mode == "detail":
            return HTML_STYLE_LIST_DETAIL
        if mode == "range":
            return HTML_STYLE_LIST_RANGE
        if mode == "daily":
            return HTML_STYLE_LIST_DAILY
