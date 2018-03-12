import os
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

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

    def send_range_email(self, date_begin, date_end, count_only=True, gather=False):
        try:
            self.read_config()
            title_line, data, total_line, type_list = StatisticsService().make_statistics(date_begin, date_end, gather)
            logger.info("统计数据Data构造成功")
            if date_begin == date_end:
                subject = "{} 网点报送汇总".format(date_begin)
                xls_file_name = os.path.join(GLOBAL_CONFIG.get_field("Excel", "xls_dir"), date_begin) + ".xls"
                html_file_name = os.path.join(GLOBAL_CONFIG.get_field("Html", "html_dir"), date_begin) + ".html"
            else:
                subject = "{} ~ {} 网点报送汇总".format(date_begin, date_end)
                xls_file_name = os.path.join(GLOBAL_CONFIG.get_field("Excel", "xls_dir"), "{} ~ {}".format(date_begin, date_end)) + ".xls"
                html_file_name = os.path.join(GLOBAL_CONFIG.get_field("Html", "html_dir"), "{} ~ {}".format(date_begin, date_end)) + ".html"
            html_content = StatisticsService().data_to_html(subject, title_line, data, total_line)
            StatisticsService().html_2_file(html_content, html_file_name)
            logger.info("html内容构造成功")
            attachment_name = StatisticsService().data_to_xls(xls_file_name, title_line, data, total_line, type_list)
            logger.info("xls内容构造成功")
        except Exception as e:
            logger.error("Error: 内容构造失败:")
            logger.error(e)
            return False
        else:
            if not count_only:
                try:
                    msg = self.make_msg('望京支行机构金融业务部', '望京支行对公团队', '每日统计_' + date_begin,  html_content, xls_file_name)
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
            else:
                return True

    @staticmethod
    def format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8'), addr))
