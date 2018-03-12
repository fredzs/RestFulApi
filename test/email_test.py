"""数据库测试文件"""


from app.api.Service.EmailService import EmailService
from app.api.Factory.LogFactory import LogFactory
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

logger = LogFactory().get_logger()




if __name__ == "__main__":
    logger.info('-----------------------------------程序开始执行-----------------------------------')
    # service = EmailService()
    # service.read_config()
    # check_result = service.send_range_email("2018-03-02", "2018-03-02")

    dcap = dict(DesiredCapabilities.PHANTOMJS)  #设置userAgent
    dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 ")

    obj = webdriver.PhantomJS() #加载网址
    obj.get('https://www.fredirox.com/wordpress/')#打开网址
    obj.save_screenshot("1.png")   #截图保存
    obj.quit()
    logger.info('-----------------------------------程序执行结束-----------------------------------')
