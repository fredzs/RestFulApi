from datetime import datetime
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

from app.api.Service.DBService import DBService
from app.api.Service.FieldsInfoService import FieldsInfoService
from app.api.Service.PerformanceService import PerformanceService


class EmailService(object):
    """Class EmailService"""
    def __init__(self):
        self._db_fields_info_service = DBService("DBFieldsInfo")

    def send_email(self):
        from_addr = "fredzs@vip.qq.com"
        password = "Fred1234,."
        to_addr = "fred_zs_icbc@163.com"
        smtp_server = "smtp.qq.com"

        request_date = datetime.today().strftime("%Y-%m-%d")

        msg = MIMEText(self.make_content(), 'html', 'utf-8')
        msg['From'] = self.format_addr('每日对公业绩统计 <%s>' % from_addr)
        msg['To'] = self.format_addr('管理员 <%s>' % to_addr)
        msg['Subject'] = Header('每日对公业绩统计_' + request_date, 'utf-8').encode()

        server = smtplib.SMTP_SSL(smtp_server, 465)
        # server.set_debuglevel(2)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()

    @staticmethod
    def format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def make_content(self):
        content = "<html><body>"
        date = str(datetime.today().strftime("%Y-%m-%d"))
        content += "<h2>" + date + " 对公业绩汇总：</h2>"
        content += "<table border=\"1\" style= \"border-collapse: collapse; border-color: #BCD1E6;\"><tbody><tr style= \"border-color: #9AA2A9;\">"
        content += "<td width=\"40\" align=\"center\"><B>序号</B></td>"
        content += "<td width=\"100\" align=\"center\"><B>网点</B></td>"

        available_fields_list = self._db_fields_info_service.db_find_list_by_attribute_list_order_by(["business", "status"],
                                                                                           ["corporate", "1"],
                                                                                           "order_index")
        for field in available_fields_list:
            content += "<td width=\"100\" align=\"center\"><B>%s</B></td>" % field.field_name
        content += "</tr>"

        performance_service = PerformanceService()
        submission_list = performance_service.pre_check_submission(date)
        for p in submission_list:
            content += "<tr><td>"
            performance = performance_service.pre_display(p)

        content += "</tbody></table>"

        content += "</body></html>"
        return content
