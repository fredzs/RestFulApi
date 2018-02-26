from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

from app.api.Service.DBService import DBService
from app.api.Service.PerformanceService import PerformanceService
import logging


class EmailService(object):
    """Class EmailService"""
    def __init__(self):
        self._db_fields_info_service = DBService("DBFieldsInfo")
        self._from_addr = "fredzs@vip.qq.com"
        self._password = "lfojfpmtjermbijj"
        self._to_addr = ["fred_zs_icbc@163.com", "38425449@qq.com", "wangjj_wj@bj.icbc.com.cn", "yuwen_wj@bj.icbc.com.cn"]
        self._smtp_server = "smtp.qq.com"

    def send_daily_email(self, date):
        try:
            msg = MIMEText(self.make_daily_content(date), 'html', 'utf-8')
            msg['From'] = self.format_addr('每日对公业绩统计 <%s>' % self._from_addr)
            msg['To'] = self.format_addr('管理员 <%s>' % self._to_addr[0])
            msg['Subject'] = Header('每日对公业绩统计_' + date, 'utf-8').encode()

            server = smtplib.SMTP_SSL(self._smtp_server, 465)
            server.login(self._from_addr, self._password)
            server.sendmail(self._from_addr, self._to_addr, msg.as_string())
        except Exception as e:
            logging.error(e)
            return False
        finally:
            server.quit()
        return True

    @staticmethod
    def format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def make_daily_content(self, date):
        content = "<html><body>"
        content += "<h2>" + date + " 对公业绩汇总：</h2>"
        content += "<table border=\"1\" style= \"border-collapse: collapse; border-color: #BCD1E6;\"><tbody><tr style= \"border-color: #9AA2A9;\">"
        content += "<td width=\"40\" align=\"center\"><B>序号</B></td>"
        content += "<td width=\"110\" align=\"center\"><B>网点</B></td>"

        try:
            available_fields_list = self._db_fields_info_service.db_find_list_by_attribute_list_order_by(["business", "status"], ["corporate", "1"], "order_index")
            a_f_id_list = []
            for field in available_fields_list:
                content += "<td width=\"70\" align=\"center\"><B>%s</B></td>" % field.field_name
                a_f_id_list.append(field.field_id)

            content += "<td width=\"100\" align=\"center\"><B>%s</B></td>" % "报送人"
            content += "</tr>"

            performance_service = PerformanceService()
            submission_list = performance_service.pre_check_submission(date)[0]
            for i, p in enumerate(submission_list):
                """第一层循环，以网点名称生成行"""
                content += "<tr>"
                content += "<td align=\"center\">" + str(i+1) + "</td>"
                content += "<td align=\"center\">" + p["dept_name"] + "</td>"

                performance_list = performance_service.find_performance_by_date_dept_name(date, p["dept_name"])
                if len(performance_list) > 0:
                    performance = performance_list[0]
                    extra_fields = performance.extra_fields
                    for a_f_id in a_f_id_list:
                        """第二层循环，以可用字段生成列"""
                        if a_f_id in extra_fields:
                            content += "<td align=\"center\">%s</td>" % extra_fields[a_f_id]
                        else:
                            content += "<td align=\"center\">-</td>"

                    content += "<td align=\"center\">%s</td>" % p["submit_user"]
                    content += "</tr>"
                else:
                    pass
        except Exception as e:
            logging.error(e)

        content += "</tbody></table>"
        content += "</body></html>"
        return content