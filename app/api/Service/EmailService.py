import os
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import xlrd, xlwt
from app.api.Service.DBService import DBService
from app.api.Factory.LogFactory import LogFactory
from app.api.Service.StatisticsService import StatisticsService
from Config import GLOBAL_CONFIG
logger = LogFactory().get_logger()


class EmailService(object):
    """Class EmailService"""
    def __init__(self):
        self._db_fields_info_service = DBService("DBFieldsInfo")
        self._from_addr = ""
        self._password = ""
        self._to_addr = []
        self._smtp_server = ""

    def read_config(self):
        self._from_addr = GLOBAL_CONFIG.get_field("Email", "from_addr")
        self._password = GLOBAL_CONFIG.get_field("Email", "password")
        self._to_addr = GLOBAL_CONFIG.get_field_list("Email", "to_addr")
        self._smtp_server = GLOBAL_CONFIG.get_field("Email", "smtp_server")

    def make_msg(self, sender_name, receiver_name, subject, html_content, attachment_name):
        msg = MIMEMultipart()
        msg['From'] = Header('%s<%s>' % (sender_name, self._from_addr), 'utf-8')
        msg['To'] = Header('%s<%s>' % (receiver_name, self._to_addr[0]), 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        # 邮件正文内容
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))
        # 构造附件
        attachment = MIMEText(open(attachment_name, 'rb').read(), 'base64', 'utf-8')
        attachment["Content-Type"] = 'application/octet-stream'
        attachment["Content-Disposition"] = "attachment; filename=%s" % attachment_name.encode("utf-8")
        msg.attach(attachment)
        return msg

    def send_range_email(self, date_begin, date_end):
        try:
            self.read_config()
            title_line, data, total_line, type_list = StatisticsService().make_statistics(date_begin, date_end)
            if date_begin == date_end:
                subject = "{}".format(date_begin)
            else:
                subject = "{}至{}".format(date_begin, date_end)
            html_content = self.data_to_html(subject, title_line, data, total_line)
            attachment_name = self.data_to_xls(subject, title_line, data, total_line, type_list)
            msg = self.make_msg('望京支行机构金融业务部', '望京支行对公团队', '每日统计_' + date_begin,  html_content, attachment_name)

            server = smtplib.SMTP_SSL(self._smtp_server, 465)
            server.login(self._from_addr, self._password)
            server.sendmail(self._from_addr, self._to_addr, msg.as_string())

        except smtplib.SMTPException as e:
            logger.error("Error: 无法发送邮件:")
            logger.error(e)
            return False
        else:
            # server.quit()
            logger.info("发送邮件成功")
            return True
        finally:
            pass

    @staticmethod
    def format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8'), addr))

    @staticmethod
    def data_to_html(subject, title_line, data, total_line):
        content = "<html><body>"
        content += "<h2>{}</h2>".format(subject)
        content += "<table border=\"1\" style= \"border-collapse: collapse; border-color: #BCD1E6;\"><tbody><tr style= \"border-color: #9AA2A9;\">"

        # 生成首行
        for title_td in title_line:
            content += "<td width=\"70\" align=\"center\">"
            content += "<p><B>{}</B></p>".format(title_td)
            content += "</td>"
        content += "</tr>"
        # 生成数据行
        for i, row in enumerate(data):
            """第一层循环，以网点名称生成行"""
            content += "<tr>"
            for col in row:
                """第二层循环，以可用字段生成列"""
                content += "<td align=\"center\">{}</td>".format(col)
            content += "</tr>"
        # 生成汇总行
        for total_td in total_line:
            content += "<td width=\"70\" align=\"center\">"
            content += "<p><B>{}</B></p>".format(total_td)
            content += "</td>"
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

        xls_file.save(file_name + ".xls")
        return file_name + ".xls"

    # def make_html_content(self, date):
    #     content = "<html><body>"
    #     content += "<h2>" + date + " 对公业绩汇总：</h2>"
    #     content += "<table border=\"1\" style= \"border-collapse: collapse; border-color: #BCD1E6;\"><tbody><tr style= \"border-color: #9AA2A9;\">"
    #     content += "<td width=\"40\" align=\"center\"><B>序号</B></td>"
    #     content += "<td width=\"110\" align=\"center\"><B>网点</B></td>"
    #
    #     try:
    #         available_fields_list = self._db_fields_info_service.db_find_list_by_attribute_list_order_by(
    #             ["business", "status"], ["corporate", "1"], "order_index")
    #         a_f_id_list = []
    #         for field in available_fields_list:
    #             content += "<td width=\"70\" align=\"center\">"
    #             if field.field_type == "int":
    #                 content += "<p><B>%s</B></p><p><B>（%s）</B></p>" % (field.field_name, field.field_unit)
    #             else:
    #                 content += "<p><B>%s</B></p>" % field.field_name
    #             content += "</td>"
    #             a_f_id_list.append(field.field_id)
    #
    #         content += "<td width=\"100\" align=\"center\"><B>%s</B></td>" % "报送人"
    #         content += "</tr>"
    #
    #         performance_service = PerformanceService()
    #         submission_list = performance_service.pre_check_submission(date)[0]
    #         for i, p in enumerate(submission_list):
    #             """第一层循环，以网点名称生成行"""
    #             content += "<tr>"
    #             content += "<td align=\"center\">" + str(i + 1) + "</td>"
    #             content += "<td align=\"center\">" + p["dept_name"] + "</td>"
    #
    #             performance_list = performance_service.find_performance_by_date(date, "dept_name", p["dept_name"])
    #             if len(performance_list) > 0:
    #                 performance = performance_list[0]
    #                 extra_fields = performance.extra_fields
    #                 for a_f_id in a_f_id_list:
    #                     """第二层循环，以可用字段生成列"""
    #                     if a_f_id in extra_fields:
    #                         content += "<td align=\"center\">%s</td>" % extra_fields[a_f_id]
    #                     else:
    #                         content += "<td align=\"center\">-</td>"
    #
    #                 content += "<td align=\"center\">%s</td>" % p["submit_user"]
    #                 content += "</tr>"
    #             else:
    #                 pass
    #     except Exception as e:
    #         logger.error(e)
    #         return ""
    #
    #     content += "</tbody></table>"
    #     content += "</body></html>"
    #     return content
