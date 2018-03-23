"""request api"""
import re
from datetime import datetime
from flask import request
from flask import render_template

from app.api.Service.ConfigService import ConfigService
from app.api.Service.DeptInfoService import DeptInfoService
from app.api.Service.EmailService import EmailService
from app.api.Service.FieldsInfoService import FieldsInfoService
from app.api.Service.PerformanceService import PerformanceService
from app.api.Service.StatisticsService import StatisticsService
from app.api.Service.UserInfoService import UserInfoService
from app.api.Service.LogService import LogService
from . import main
from app.api.Factory.LogFactory import LogFactory
from Config import GLOBAL_CONFIG

logger = LogFactory().get_logger()


@main.route('/')
@main.route('/api')
def index():
    """默认的Get请求"""
    logger.info('')
    log_service = LogService()
    log_service.submit_log("admin", "Server", "/api", "http_get", "")
    logger.info('---------收到index页面请求：/api，已记录日志。----------')

    request_date = datetime.today().strftime("%Y-%m-%d")
    logger.info('---------index页面请求处理完毕-----------')
    return render_template("api_list.html", base_url="", title='api List', date=request_date, dept_name='支行营业室',
                           admin_password="159357")


@main.route('/test')
@main.route('/test/api')
def test():
    """默认的Get请求"""
    logger.info('')
    log_service = LogService()
    log_service.submit_log("admin", "/test/api", "/test/api", "http_get", "")
    logger.info('---------收到index页面请求：/api----------')

    request_date = datetime.today().strftime("%Y-%m-%d")
    logger.info('---------index页面请求处理完毕-----------')
    return render_template("/test/api_list.html", title='api List', date=request_date, dept_name='支行营业室',
                           admin_password="159357")


@main.route('/api/log', methods=['POST'])
@main.route('/test/api/log', methods=['POST'])
def add_log():
    """POST方法，用于记录日志"""
    logger.info('---------收到POST请求：/api/log，记录日志。----------')
    result = False
    logger.info("data: user_name='%s', page='%s', method='%s', content='%s'" % (
        request.json["user_name"], request.json["page"], request.json["method"], request.json["content"]))
    try:
        log_service = LogService()
        result = log_service.submit_log(request.json["user_name"], request.json["page"], "web_page", request.json["method"], request.json["content"])
    except Exception as e:
        logger.error('发生错误!')
        logger.error(e)
    finally:
        if result:
            logger.info('POST请求/api/log处理完毕，返回值%s' % "success")
            return "success", 201  # 并返回这个添加的task内容，和状态码
        else:
            logger.info('POST请求/api/log处理完毕，返回值%s' % "fail")
            return "fail", 500


@main.route('/api/performance', methods=['POST'])
@main.route('/test/api/performance', methods=['POST'])
def add_performance():
    """POST方法，用于提交业绩"""
    logger.info('')
    logger.info('---------收到来POST请求：/api/performance----------')

    if not request.json or 'dept_id' not in request.json:
        # 如果请求里面没有JSON数据，或者在JSON数据里面dept_id的内容是空的
        logger.info("传入参数错误！")
        return "args_missing", 500
    if 'user_name' in request.json:
        user_name = request.json["user_name"]
    else:
        user_name = "admin"
    log_service = LogService()
    page = request.json["page"]
    log_service.submit_log(user_name, page, "/api/performance", "http_post", request.json)
    if user_name == "None" or user_name == "null":
        user_name = "unknown"
    logger.info('用户[%s]提交业绩：' % user_name)
    logger.info("data: dept_id='%s', date='%s', submit_user='%s', extra_fields='%s'" % (
        request.json["dept_id"], request.json["date"], request.json["submit_user"], request.json["extra_fields"]))

    result = False
    try:
        service = PerformanceService()
        result = service.submit_performance(request.json)
    except Exception as e:
        logger.error('发生错误!')
        logger.error(e)
    finally:
        if result:
            logger.info('POST请求/api/performance处理完毕，返回值%s' % "success")
            return "success", 201  # 并返回这个添加的task内容，和状态码
        else:
            logger.info('POST请求/api/performance处理完毕，返回值%s' % "fail")
            return "fail", 500


@main.route('/api/update_field', methods=['POST'])
@main.route('/test/api/update_field', methods=['POST'])
def update_field():
    """POST方法，用于更新字段"""
    logger.info('')
    logger.info('---------收到POST请求：/api/update_field----------')

    if not request.json or 'field_id' not in request.json:
        logger.info("传入参数错误！")
        return "args_missing", 500
    if 'user_name' in request.json:
        user_name = request.json["user_name"]
    else:
        user_name = "admin"
    log_service = LogService()
    page = request.json["page"]
    log_service.submit_log(user_name, page, "/api/update_field", "http_post", request.json)
    logger.info('用户[%s]修改字段：' % user_name)
    logger.info("data: field_id=%s, update_key=%s, update_value=%s" % (
        request.json["field_id"], request.json["update_k"], request.json["update_v"]))
    result = False
    try:
        service = FieldsInfoService()
        result = service.update_field(request.json)
    except Exception as e:
        logger.error('发生错误!')
        logger.error(e)
    finally:
        if result:
            logger.info('POST请求/api/update_field处理完毕，返回值%s' % "success")
            return "success", 201
        else:
            logger.info('POST请求/api/update_field处理完毕，返回值%s' % "fail")
            return "fail", 500


@main.route('/api/create_field', methods=['POST'])
@main.route('/test/api/create_field', methods=['POST'])
def create_field():
    """POST方法，用于更新字段"""
    logger.info('')
    logger.info('---------收到POST请求：/api/create_field----------')

    if not request.json or 'field_name' not in request.json or 'field_type' not in request.json or 'field_unit' not in request.json:
        logger.info("传入参数错误！")
        return "args_missing", 500
    if 'user_name' in request.json:
        user_name = request.json["user_name"]
    else:
        user_name = "admin"
    log_service = LogService()
    page = request.json["page"]
    log_service.submit_log(user_name, page, "/api/create_field", "http_post", request.json)
    logger.info('用户[%s]新增字段：' % user_name)
    logger.info("data: field_name=%s, field_type=%s, field_unit=%s" % (
        request.json["field_name"], request.json["field_type"], request.json["field_unit"]))

    result = False
    try:
        service = FieldsInfoService()
        result = service.create_field(request.json)
    except Exception as e:
        logger.error('发生错误!')
        logger.error(e)
    finally:
        if result:
            logger.info('POST请求/api/create_field处理完毕，返回值%s' % "success")
            return "success", 201
        else:
            logger.info('POST请求/api/create_field处理完毕，返回值%s' % "fail")
            return "fail", 500


@main.route('/api/sort_field', methods=['POST'])
@main.route('/test/api/sort_field', methods=['POST'])
def sort_field():
    """POST方法，用于给字段排序"""
    logger.info('')
    logger.info('---------收到POST请求：/api/sort_field----------')

    if not request.json or 'new_order' not in request.json:
        logger.info("传入参数错误！")
        return "args_missing", 500
    if 'user_name' in request.json:
        user_name = request.json["user_name"]
    else:
        user_name = "admin"
    log_service = LogService()
    page = request.json["page"]
    log_service.submit_log(user_name, page, "/api/sort_field", "http_post", request.json)
    logger.info('用户[%s]重新排序字段：' % user_name)
    logger.info("data: new_order=%s" % request.json["new_order"])

    result = False
    try:
        service = FieldsInfoService()
        result = service.sort_field(request.json)
    except Exception as e:
        logger.error('发生错误!')
        logger.error(e)
    finally:
        if result:
            logger.info('POST请求/api/sort_field处理完毕，返回值%s' % "success")
            return "success", 201
        else:
            logger.info('POST请求/api/sort_field处理完毕，返回值%s' % "fail")
            return "fail", 500


@main.route('/api/statistics', methods=['GET'])
@main.route('/test/api/statistics', methods=['GET'])
def make_statistics():
    """POST方法，用于给字段排序"""
    logger.info('')
    logger.info('---------收到GET请求：/api/statistics----------')

    if not request.args:
        logger.info("传入参数错误！")
        return "args_missing", 500
    else:
        date_begin = request.args.get("date_begin")
        date_end = request.args.get("date_end")
        mode = request.args.get("mode")
    if request.args.get('user_name') is not None:
        user_name = request.args.get('user_name')
    else:
        user_name = "admin"
    log_service = LogService()
    page = request.args.get('page')
    log_content = request.args.get('content')
    log_service.submit_log(user_name, page, "/api/statistics", "http_get", log_content)
    logger.info("用户[%s]请求统计业绩：" % user_name)
    logger.info("data: date_begin=%s, date_end=%s, mode=%s" % (date_begin, date_end, mode))

    result = False
    try:
        service = StatisticsService()
        GLOBAL_CONFIG.reload_config_file()
        result = service.create_files(date_begin, date_end, mode)
    except Exception as e:
        logger.error('发生错误!')
        logger.error(e)
    finally:
        if result:
            logger.info('GET请求/api/statistics 处理完毕，返回值%s' % "success")
            return "success", 201
        else:
            logger.info('GET请求/api/statistics 处理失败，返回值%s' % "fail")
            return "fail", 500


@main.route('/api/email', methods=['GET'])
@main.route('/test/api/email', methods=['GET'])
def send_email():
    """GET方法，用于获取邮件"""
    logger.info('')
    logger.info('---------收到POST请求：/api/email----------')

    if not request.json or 'date_begin' not in request.json or 'date_end' not in request.json or 'mode' not in request.json:
        logger.info("传入参数错误！")
        return "args_missing", 500
    else:
        date_begin = request.json["date_begin"]
        date_end = request.json["date_end"]
        if request.json["count_only"] == "true":
            count_only = True
        else:
            count_only = False
    if 'user_name' in request.json:
        user_name = request.json["user_name"]
    else:
        user_name = "admin"
    log_service = LogService()
    page = request.json["page"]
    log_service.submit_log(user_name, page, "/api/send_range_email", "http_post", request.json)
    logger.info("用户[%s]请求统计业绩：" % user_name)
    logger.info("data: date_begin=%s, date_end=%s, count_only=%s" % (date_begin, date_end, count_only))

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
        if result:
            logger.info('POST请求/api/send_range_email处理完毕，返回值%s' % "success")
            return "success", 201
        else:
            logger.info('POST请求/api/send_range_email处理失败，返回值%s' % "fail")
            return "fail", 500


@main.route('/api/check', methods=['GET'])
@main.route('/test/api/check', methods=['GET'])
def check_submit():
    """GET，用于检查未提交业绩的网点"""
    logger.info('')
    logger.info('---------收到GET请求：/api/check----------')

    if not request.args.get('date'):
        request_date = datetime.today().strftime("%Y-%m-%d")
    else:
        request_date = request.args.get('date')
    if request.args.get('user_name') is not None:
        user_name = request.args.get('user_name')
    else:
        user_name = "admin"
    log_service = LogService()
    page = request.args.get('page')
    log_content = "date=%s" % request_date
    log_service.submit_log(user_name, page, "/api/check", "http_get", log_content)
    logger.info('用户[%s]查询当日业绩报送情况。' % user_name)
    logger.info("data: date=%s" % request_date)

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
        logger.info('POST请求/api/check处理完毕。')
        return check_result, 500
    finally:
        logger.info('POST请求/api/check处理完毕')
        return check_result, 201


@main.route('/api/branches', methods=['GET'])
@main.route('/test/api/branches', methods=['GET'])
def get_branches():
    """GET，用于获取所有网点"""
    logger.info('')
    logger.info('---------收到GET请求：/api/branches----------')

    if not request.args.get('branch_name'):
        branch_name = "wangjing"
    else:
        branch_name = "wangjing"
    if request.args.get('user_name') is not None:
        user_name = request.args.get('user_name')
    else:
        user_name = "admin"
    log_service = LogService()
    page = request.args.get('page')
    log_service.submit_log(user_name, page, "/api/branches", "http_get", "")
    logger.info('用户[%s]查询所有网点：' % user_name)
    logger.info("data: date=%s" % branch_name)

    branch_list = []
    try:
        dept_info_service = DeptInfoService()
        branch_list = dept_info_service.find_branch_list(branch_name)
    except Exception as e:
        logger.error('发生错误!')
        logger.error(e)
        return [], 500
    finally:
        logger.info('POST请求/api/branches处理完毕，返回值正常。')
        return branch_list, 201


@main.route('/api/fields', methods=['GET'])
@main.route('/test/api/fields', methods=['GET'])
def get_fields():
    """GET，用于获取所有字段"""
    logger.info('')
    logger.info('---------收到GET请求：/api/fields----------')
    if request.args.get('user_name') is not None:
        user_name = request.args.get('user_name')
    else:
        user_name = "admin"
    log_service = LogService()
    page = request.args.get('page')
    log_service.submit_log(user_name, page, "/api/fields", "http_post", "")
    logger.info('用户[%s]查看所有字段：' % user_name)
    fields_list = []
    try:
        fields_info_service = FieldsInfoService()
        fields_list = fields_info_service.find_fields_list()
    except Exception as e:
        logger.error('发生错误!')
        logger.error(e)
        return [], 500
    finally:
        logger.info('POST请求/api/fields处理完毕，返回值正常。')
        return fields_list, 201


@main.route('/api/fields_name', methods=['GET'])
@main.route('/test/api/fields_name', methods=['GET'])
def get_available_fields_name():
    """GET，用于获取所有可用字段"""
    logger.info('')
    logger.info('---------收到GET请求：/api/fields_name----------')
    if request.args.get('user_name') is not None:
        user_name = request.args.get('user_name')
    else:
        user_name = "admin"
    log_service = LogService()
    page = request.args.get('page')
    log_service.submit_log(user_name, page, "/api/fields_name", "http_get", "")
    logger.info('用户[%s]查询所有字段名。' % user_name)
    fields_list = []
    try:
        fields_info_service = FieldsInfoService()
        fields_list = fields_info_service.find_available_fields_name()
    except Exception as e:
        logger.error('发生错误!')
        logger.error(e)
        return [], 500
    finally:
        logger.info('POST请求/api/fields_name处理完毕，返回值正常。')
        return fields_list, 201


@main.route('/api/performance', methods=['GET'])
@main.route('/test/api/performance', methods=['GET'])
def display_performance():
    """GET，用于查询单日业绩"""
    logger.info('')
    logger.info('---------收到GET请求：/api/display----------')

    if not request.args.get('date'):
        request_date = datetime.today().strftime("%Y-%m-%d")
    else:
        request_date = request.args.get('date')

    if not request.args.get('dept_name'):
        logger.info("传入参数错误！")
        return "args_missing", 500
    else:
        request_dept_name = request.args.get('dept_name')
    date = datetime.strptime(request_date, "%Y-%m-%d")
    if request.args.get('user_name') is not None:
        user_name = request.args.get('user_name')
    else:
        user_name = "admin"
    log_service = LogService()
    page = request.args.get('page')
    log_content = "date=%s, dept_name=%s" % (request_date, request_dept_name)
    log_service.submit_log(user_name, page, "/api/display", "http_get", log_content)
    logger.info('用户[%s]查询单日业绩。' % user_name)
    logger.info("data: date=%s, dept_name=%s" % (request_date, request.args.get('dept_name')))

    performance = {}
    try:
        performance_service = PerformanceService()
        performance = performance_service.display(date, request_dept_name)
    except Exception as e:
        logger.error('发生错误!')
        logger.error(e)
        return {}, 500
    finally:
        logger.info('POST请求/api/display处理完毕，返回值正常。')
        return performance, 201


@main.route('/api/find', methods=['GET'])
@main.route('/test/api/find', methods=['GET'])
def find():
    """GET，用于查找一条业绩"""
    logger.info('')
    logger.info('---------收到GET请求：/api/find----------')

    if not request.args.get('date') or not request.args.get("dept_id"):
        logger.info("传入参数错误！")
        return "args_missing", 500
    else:
        request_date = request.args.get('date')
        request_dept_id = request.args.get('dept_id')

    date = datetime.strptime(request_date, "%Y-%m-%d")
    if request.args.get('user_name') is not None:
        user_name = request.args.get('user_name')
    else:
        user_name = "admin"
    log_service = LogService()
    page = request.args.get('page')
    log_content = "date=%s, dept_id=%s" % (request_date, request_dept_id)
    log_service.submit_log(user_name, page, "/api/find", "http_get", log_content)
    logger.info('用户[%s]预提交业绩查询。' % user_name)
    logger.info("data: date=%s, dept_id=%s" % (request_date, request_dept_id))

    result = {}
    try:
        performance_service = PerformanceService()
        result = performance_service.find(date, request_dept_id)
    except Exception as e:
        logger.error('发生错误!')
        logger.error(e)
        return {}, 500
    finally:
        logger.info('POST请求/api/find处理完毕，返回值%s' % str(result))
        return result, 201


@main.route('/api/admin', methods=['GET'])
@main.route('/test/api/admin', methods=['GET'])
def admin():
    """GET，用于检查管理员密码是否正确"""
    logger.info('')
    logger.info('---------收到GET请求：/api/admin----------')

    logger.info(request.args)
    if not request.args.get('admin_password'):
        logger.info("传入参数错误！")
        return "args_missing", 500
    else:
        admin_password = request.args.get('admin_password')
    if request.args.get('user_name') is not None:
        user_name = request.args.get('user_name')
    else:
        user_name = "admin"
    log_service = LogService()
    page = request.args.get('page')
    log_content = "avatar_url=%s" % (request.args.get('admin_password'))
    log_service.submit_log(user_name, page, "/api/admin", "http_get", log_content)
    logger.info('用户[%s]请求登陆管理员界面。' % user_name)
    logger.info("data: admin_password=%s" % admin_password)

    result = False
    try:
        config_service = ConfigService()
        result = config_service.check_password(admin_password)
    except Exception as e:
        logger.error('发生错误!')
        logger.error(e)
        return "error", 500
    finally:
        logger.info('密码验证结果：' + str(result))
        logger.info('---------GET请求处理完毕-----------')
        if result:
            logger.info('POST请求/api/admin处理完毕，返回值%s' % "access")
            return "access", 201
        else:
            logger.info('POST请求/api/admin处理完毕，返回值%s' % "forbid")
            return "forbid", 201


@main.route('/api/dept', methods=['GET'])
@main.route('/test/api/dept', methods=['GET'])
def dept():
    """GET，用于通过用户名获取所在单位"""
    logger.info('')
    logger.info('---------收到GET请求：/api/dept----------')

    logger.info(request.args)
    if not request.args.get('user_name') or not request.args.get('dept_id'):
        logger.info("传入参数错误！")
        return "args_missing", 500
    else:
        user_name = request.args.get('user_name')
        dept_id = request.args.get('dept_id')
    log_service = LogService()
    page = request.args.get('page')
    log_content = "dept_id=%s" % (request.args.get('dept_id'))
    log_service.submit_log(user_name, page, "/api/dept", "http_get", log_content)
    logger.info('用户[%s]查询所在单位。' % user_name)
    logger.info("data: user_name=%s, dept_id=%s" % (user_name, dept_id))

    dept_service = DeptInfoService()
    result = False

    try:
        result = dept_service.find_dept_info(dept_id)
    except Exception as e:
        logger.error('发生错误!')
        logger.error(e)
        return dept_service.obj_2_json({}), 500
    finally:
        logger.info('POST请求/api/dept处理完毕，返回值%s' % str(result))
        return result, 201


@main.route('/api/user', methods=['GET'])
@main.route('/test/api/user', methods=['GET'])
def user():
    """GET，用于通过用户名获取所在单位"""
    logger.info('')
    logger.info('---------收到GET请求：/api/user----------')

    logger.info(request.args)
    if not request.args.get('nick_name'):
        logger.info("传入参数错误！")
        return "args_missing", 500
    else:
        nick_name = request.args.get('nick_name')
    if request.args.get('avatar_url') != "None":
        logger.info("用户头像URL为：[%s]" % request.args.get('avatar_url'))
    logger.info("用户[%s]登陆，查找用户信息。" % nick_name)
    if nick_name == 'null' or nick_name == 'None':
        nick_name = "unknown"
    log_service = LogService()
    page = request.args.get('page')
    log_content = "avatar_url=%s" % (request.args.get('avatar_url'))
    log_service.submit_log(nick_name, page, "/api/user", "http_get", log_content)
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
        logger.info('POST请求/api/user处理完毕，返回值%s' % str(result))
        return result, 201
