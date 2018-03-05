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
        attachment["Content-Disposition"] = "attachment; filename=%s" % attachment_name
        msg.attach(attachment)
        return msg

    def send_range_email(self, date_begin, date_end):
        try:
            self.read_config()
            title_line, data, total_line, type_list = StatisticsService().make_statistics(date_begin, date_end)
            logger.info("统计数据构造成功")
            if date_begin == date_end:
                subject = "{} 网点报送汇总".format(date_begin)
                xls_file_name = os.path.join(GLOBAL_CONFIG.get_field("Excel", "xls_dir"), date_begin) + ".xls"
                html_file_name = os.path.join(GLOBAL_CONFIG.get_field("Html", "html_dir"), date_begin) + ".html"
            else:
                subject = "{} ~ {} 网点报送汇总".format(date_begin, date_end)
                xls_file_name = os.path.join(GLOBAL_CONFIG.get_field("Excel", "xls_dir"),"{} ~ {}".format(date_begin, date_end)) + ".xls"
                html_file_name = os.path.join(GLOBAL_CONFIG.get_field("Html", "html_dir"),"{} ~ {}".format(date_begin, date_end)) + ".html"
            html_content = self.data_to_html(subject, title_line, data, total_line)
            self.html_2_file(html_content, html_file_name)
            logger.info("html内容构造成功")
            attachment_name = self.data_to_xls(xls_file_name, title_line, data, total_line, type_list)
            logger.info("xls内容构造成功")
            msg = self.make_msg('望京支行机构金融业务部', '望京支行对公团队', '每日统计_' + date_begin,  html_content, xls_file_name)

            # server = smtplib.SMTP_SSL(self._smtp_server, 465)
            # server.login(self._from_addr, self._password)
            # server.sendmail(self._from_addr, self._to_addr, msg.as_string())

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
    def html_2_file(html, file_name):
        with open(file_name, 'w') as f:
            f.write(html)

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
        content += "<tr>"
        for total_td in total_line:
            content += "<td align=\"center\"><p><B>{}</B></p></td>".format(total_td)
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
