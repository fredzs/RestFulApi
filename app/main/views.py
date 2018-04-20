"""request api"""
import re
from datetime import datetime

from flask import g
from flask import render_template
from flask import request
from werkzeug.exceptions import abort

from Config import GLOBAL_CONFIG
from app.api.Factory.LogFactory import LogFactory
from app.api.Service.ConfigService import ConfigService
from app.api.Service.DeptInfoService import DeptInfoService
from app.api.Service.EmailService import EmailService
from app.api.Service.FieldsInfoService import FieldsInfoService
from app.api.Service.LogService import LogService
from app.api.Service.PerformanceService import PerformanceService
from app.api.Service.StatisticsService import StatisticsService
from app.api.Service.UserInfoService import UserInfoService
from . import main

logger = LogFactory().get_logger()


@main.before_request
def before_request():
    skip_path = ["/api", "/icbc", "/api/log", "/test/api", "/test/icbc", "/test/api/log"]
    if request.path in skip_path:
        return

    # 0. init para
    bad_request = False
    g.path = request.path
    g.method = request.method
    if g.method == "POST" or g.method == "PUT":
        g.data = request.json
    elif g.method == "GET":
        g.data = multi_dict_2_dict(request.args)
    g.user_name = g.data["user_name"] if ("user_name" in g.data) else "admin"
    page = g.data["page"] if ("page" in g.data) else "{}{}".format("/WebServer", g.path)
    resource = g.path
    method = "HTTP_{}".format(g.method)
    content = g.data["content"] if ("content" in g.data) else g.data

    # 2. print logs
    logger.info('------------------------------------------------')
    logger.info('收到用户[{}]的[{}]请求[{}]'.format(g.user_name, g.method, g.path))
    logger.info('参数列表:{}'.format(g.data))

    # 3. save logs to DB
    log_service = LogService()
    log_service.submit_log(g.user_name, page, resource, method, content)
    logger.info('已记录日志。')

    if bad_request:
        abort(400)


@main.after_request
def after_request(response):
    skip_path = ["/api", "/icbc", "/api/log"]
    if request.path in skip_path:
        return response
    # response = make_response("success", 200)
    if g.method == "GET":
        logger.info('[{}]请求[{}]处理完毕，返回值<{}>'.format(g.method, g.path, response.status))
    elif g.method == "POST" or g.method == "PUT":
        logger.info('[{}]请求[{}]处理完毕，返回值<{}, {}>'.format(g.method, g.path, response.data, response.status))
    return response


@main.route('/icbc')
def index():
    """默认的Get请求"""
    date_begin = request.args.get("date_begin")
    date_end = request.args.get("date_end")
    mode = request.args.get("mode")
    service = StatisticsService()
    GLOBAL_CONFIG.reload_config_file()
    title_line, data, total_line, type_list = service.get_data_from_db(date_begin, date_end, mode)
    logger.info('GET请求/api/icbc 处理完毕，返回值%s' % "success")
    return render_template("dashboard.html", title_line=title_line, data=data, total_line=total_line)


@main.route('/api')
def api_list():
    """默认的Get请求"""
    log_service = LogService()
    log_service.submit_log("admin", "/WebServer/api", "web_page", "http_get", "浏览页面")
    request_date = datetime.today().strftime("%Y-%m-%d")
    return render_template("api_list.html", base_url="", title='api List', date=request_date, dept_name='支行营业室',
                           admin_password="159357")


# @main.route('/test/api')
# def api_list_test():
#     """默认的Get请求"""
#     log_service = LogService()
#     log_service.submit_log("admin", "/test/api", "/test/api", "http_get", "")
#     request_date = datetime.today().strftime("%Y-%m-%d")
#     return render_template("/test/api_list.html", title='api List', date=request_date, dept_name='支行营业室',
#                            admin_password="159357")
#

'''''''''''''''''''''''''''''''''[POST请求]'''''''''''''''''''''''''''''''''''''''''''''''''''


@main.route('/api/performance', methods=['GET'])
@main.route('/test/api/performance', methods=['GET'])
def display_performance():
    """GET，用于查询单日业绩"""
    if not check_args(['dept_name']):
        return "args_missing: dept_name", 400
    request_dept_name = g.data['dept_name']
    request_date = datetime.today().strftime("%Y-%m-%d") if 'date' not in g.data else g.data['date']
    date = datetime.strptime(request_date, "%Y-%m-%d")
    logger.info('用户[%s]查询单日业绩。' % g.user_name)

    result = {}
    try:
        performance_service = PerformanceService()
        result = performance_service.display(date, request_dept_name)
    except Exception as e:
        logger.error('发生错误!')
        logger.error(e)
        return {}, 500
    finally:
        return result, 201


@main.route('/api/performance', methods=['POST'])
@main.route('/test/api/performance', methods=['POST'])
def add_performance():
    """POST方法，用于提交业绩"""
    if not check_args(['dept_id']):
        return "args_missing", 400
    if g.user_name == "None" or g.user_name == "null":
        g.user_name = "unknown"
    logger.info('用户[%s]提交业绩：' % g.user_name)

    result = False
    try:
        service = PerformanceService()
        result = service.submit_performance(g.data)
    except Exception as e:
        logger.error('发生错误!')
        logger.error(e)
    finally:
        return ("success", 201) if result else ("fail", 500)


@main.route('/api/submission', methods=['GET'])
@main.route('/test/api/submission', methods=['GET'])
def check_submit():
    """GET，用于检查未提交业绩的网点"""
    logger.info('用户[%s]查询当日业绩报送情况。' % g.user_name)
    request_date = datetime.today().strftime("%Y-%m-%d") if 'date' not in g.data else g.data['date']
    check_result = PerformanceService().obj_2_json({"date": "", "submission_list": [], "unsubmission_list": []})
    try:
        date = datetime.strptime(request_date, "%Y-%m-%d")
        performance_service = PerformanceService()
        check_result = performance_service.check_submission(date)
    except ValueError:
        logger.warning('日期选择错误')
        return check_result, 201
    except Exception as e:
        logger.error('发生错误!')
        logger.error(e)
        return check_result, 500
    finally:
        return check_result, 201


@main.route('/api/branches', methods=['GET'])
@main.route('/test/api/branches', methods=['GET'])
def get_branches():
    """GET，用于获取所有网点"""
    logger.info('用户[%s]查询所有网点：' % g.user_name)
    branch_name = "wangjing" if 'branch_name' not in g.data else "wangjing"
    branch_list = []
    try:
        dept_info_service = DeptInfoService()
        branch_list = dept_info_service.find_branch_list(branch_name)
    except Exception as e:
        logger.error('发生错误!')
        logger.error(e)
        return [], 500
    finally:
        return branch_list, 201


@main.route('/api/dept', methods=['GET'])
@main.route('/test/api/dept', methods=['GET'])
def dept():
    """GET，用于通过单位id获取所在单位"""
    if not check_args(['dept_id']):
        return "args_missing", 400
    dept_id = g.data['dept_id']
    logger.info('用户[%s]查询所在单位。' % g.user_name)

    dept_service = DeptInfoService()
    result = False
    try:
        result = dept_service.find_dept_info(dept_id)
    except Exception as e:
        logger.error('发生错误!')
        logger.error(e)
        return dept_service.obj_2_json({}), 500
    finally:
        logger.info(str(result))
        return result, 200


@main.route('/api/fields', methods=['GET'])
@main.route('/test/api/fields', methods=['GET'])
def get_fields():
    """GET，用于获取所有字段"""
    logger.info('用户[%s]查看所有字段：' % g.user_name)
    fields_list = []
    try:
        fields_info_service = FieldsInfoService()
        fields_list = fields_info_service.find_fields_list()
    except Exception as e:
        logger.error('发生错误!')
        logger.error(e)
        return [], 500
    finally:
        return fields_list, 201


@main.route('/api/fields', methods=['POST'])
@main.route('/test/api/fields', methods=['POST'])
def create_field():
    """POST方法，用于创建字段"""
    if not check_args(['field_name', "field_type", 'field_unit']):
        return "args_missing", 400
    logger.info('用户[%s]新增字段：' % g.user_name)

    result = False
    try:
        service = FieldsInfoService()
        result = service.create_field(g.data)
    except Exception as e:
        logger.error('发生错误!')
        logger.error(e)
    finally:
        return ("success", 201) if result else ("fail", 500)


@main.route('/api/fields/<string:field_id>', methods=['PUT'])
@main.route('/test/api/fields/<string:field_id>', methods=['PUT'])
def update_field(field_id):
    """POST方法，每次调用，更新字段的一个属性"""
    logger.info('用户[%s]修改字段：' % g.user_name)

    result = False
    try:
        service = FieldsInfoService()
        result = service.update_field(field_id, g.data)
    except Exception as e:
        logger.error('发生错误!')
        logger.error(e)
    finally:
        return ("success", 201) if result else ("fail", 500)


@main.route('/api/logs', methods=['POST'])
@main.route('/test/api/logs', methods=['POST'])
def add_log():
    """POST方法，用于记录日志，格式：
    1.小程序调用API: (user_name, g.path,                 "/api/user",    "http_get", g.data)
    2.小程序页面:    (user_name, "/WeChat/Check/Check",  "wechat_page",  "browse",   "每日报送页面")
    3.浏览器调用API: (user_name, g.path,                 "/api/user",    "http_get", g.data)
    4.浏览器页面:    (user_name, "/WebServer/api",          "web_page",     "http_get", "浏览页面")"""
    logger.info('---------收到POST请求：/api/log，记录日志。----------')
    result = False
    logger.info("data: user_name='%s', page='%s', method='%s', content='%s'" % (
        request.json["user_name"], request.json["page"], request.json["method"], request.json["content"]))
    try:
        log_service = LogService()
        result = log_service.submit_log(request.json["user_name"], request.json["page"], "wechat_page",
                                        request.json["method"], request.json["content"])
    except Exception as e:
        logger.error('发生错误!')
        logger.error(e)
    finally:
        return ("success", 201) if result else ("fail", 500)





@main.route('/api/sort_field', methods=['POST'])
@main.route('/test/api/sort_field', methods=['POST'])
def sort_field():
    """POST方法，用于给字段排序"""
    if not check_args(['new_order']):
        return "args_missing", 400
    logger.info('用户[%s]重新排序字段：' % g.user_name)

    result = False
    try:
        service = FieldsInfoService()
        result = service.sort_field(g.data)
    except Exception as e:
        logger.error('发生错误!')
        logger.error(e)
    finally:
        return ("success", 201) if result else ("fail", 500)


@main.route('/api/statistics', methods=['POST'])
@main.route('/test/api/statistics', methods=['POST'])
def make_statistics():
    """POST方法，用于生成统计信息"""
    if not check_args(['date_begin', "date_end", 'mode']):
        return "args_missing", 400
    date_begin, date_end, mode = g.data["date_begin"], g.data["date_end"], g.data["mode"]
    logger.info("用户[%s]请求统计业绩：" % g.user_name)

    result = False
    try:
        service = StatisticsService()
        GLOBAL_CONFIG.reload_config_file()
        result = service.create_files(date_begin, date_end, mode)
    except Exception as e:
        logger.error('发生错误!')
        logger.error(e)
    finally:
        return ("success", 201) if result else ("fail", 500)


@main.route('/api/emails', methods=['POST'])
@main.route('/test/api/emails', methods=['POST'])
def send_email():
    """POST方法，用于获取邮件"""
    if not check_args(['date_begin', "date_end", 'mode']):
        return "args_missing", 400
    date_begin, date_end = g.data["date_begin"], g.data["date_end"]
    count_only = True if (g.data["count_only"] == "true") else False
    logger.info("用户[%s]请求发送业绩统计邮件：" % g.user_name)

    result = False
    try:
        service = EmailService()
        mode = GLOBAL_CONFIG.get_field("Setting", "mode")
        GLOBAL_CONFIG.reload_config_file()
        if mode == "test":
            GLOBAL_CONFIG.set_field("Setting", "mode", mode)
        result = service.send_range_email(date_begin, date_end, count_only)
    except Exception as e:
        logger.error('发生错误!')
        logger.error(e)
    finally:
        return ("success", 201) if result else ("fail", 500)


'''''''''''''''''''''''''''''''''[GET请求]'''''''''''''''''''''''''''''''''''''''''''''''''''






@main.route('/api/fields_name', methods=['GET'])
@main.route('/test/api/fields_name', methods=['GET'])
def get_available_fields_name():
    """GET，用于获取所有可用字段"""
    logger.info('用户[%s]查询所有字段名。' % g.user_name)
    fields_list = []
    try:
        fields_info_service = FieldsInfoService()
        fields_list = fields_info_service.find_available_fields_name()
    except Exception as e:
        logger.error('发生错误!')
        logger.error(e)
        return [], 500
    finally:
        return fields_list, 201




@main.route('/api/performance_submit_info', methods=['GET'])
@main.route('/test/api/performance_submit_info', methods=['GET'])
def find():
    """GET，用于查找一条业绩"""
    if not check_args(['date', "dept_id"]):
        return "args_missing", 400
    request_date = g.data['date']
    request_dept_id = g.data['dept_id']
    date = datetime.strptime(request_date, "%Y-%m-%d")
    logger.info('用户[%s]预提交业绩查询。' % g.user_name)

    result = {}
    try:
        performance_service = PerformanceService()
        result = performance_service.find(date, request_dept_id)
    except Exception as e:
        logger.error('发生错误!')
        logger.error(e)
        return {}, 500
    finally:
        return result, 201


@main.route('/api/admin', methods=['GET'])
@main.route('/test/api/admin', methods=['GET'])
def admin():
    """GET，用于检查管理员密码是否正确"""
    if not check_args(['admin_password']):
        return "args_missing", 400
    admin_password = g.data['admin_password']
    logger.info('用户[%s]请求登陆管理员界面。' % g.user_name)

    result = False
    try:
        config_service = ConfigService()
        result = config_service.check_password(admin_password)
    except Exception as e:
        logger.error('发生错误!')
        logger.error(e)
        return "error", 500
    finally:
        return ("success", 201) if result else ("fail", 500)


@main.route('/api/users', methods=['GET'])
@main.route('/test/api/users', methods=['GET'])
def user():
    """GET，用于通过用户昵称获取所在单位"""
    if not check_args(['nick_name']):
        return "args_missing", 400
    nick_name = g.data['nick_name']
    if g.data['avatar_url'] != "None":
        logger.info("用户头像URL为：[%s]" % g.data['avatar_url'])
    logger.info("用户[%s]登陆，查找用户信息。" % nick_name)
    if nick_name == 'null' or nick_name == 'None':
        nick_name = "unknown"

    emoji_pattern = re.compile(
        '(\ud83d[\ude00-\ude4f])|'  # emoticons
        '(\ud83c[\udf00-\uffff])|'  # symbols & pictographs (1 of 2)
        '(\ud83d[\u0000-\uddff])|'  # symbols & pictographs (2 of 2)
        '(\ud83d[\ude80-\udeff])|'  # transport & map symbols
        '(\ud83c[\udde0-\uddff])'  # flags (iOS)
        '+', flags=re.UNICODE)

    new_nick_name = emoji_pattern.sub(r'', nick_name)
    logger.info("data: nick_name=%s, 过滤特殊字符后nick_name=%s" % (nick_name, new_nick_name))

    user_service = UserInfoService()
    result = user_service.obj_2_json({})
    try:
        result = user_service.find_user_info("wx_nick_name", new_nick_name)
        if request == 'null':
            pass
    except Exception as e:
        logger.error('发生错误!')
        logger.error(e)
        return user_service.obj_2_json({}), 500
    finally:
        logger.info(str(result))
        return result, 200


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


def check_args(args_list):
    for arg in args_list:
        if arg not in g.data:
            logger.info("传入参数错误！")
            return False
    return True


def multi_dict_2_dict(multi_dict):
    result = {}
    for key in multi_dict:
        result[key] = multi_dict[key]
    return result
