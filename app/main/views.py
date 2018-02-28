"""request api"""

from datetime import datetime
from flask import request
from flask import render_template

from app.api.Service.ConfigService import ConfigService
from app.api.Service.DeptInfoService import DeptInfoService
from app.api.Service.EmailService import EmailService
from app.api.Service.FieldsInfoService import FieldsInfoService
from app.api.Service.PerformanceService import PerformanceService
from . import main
from app.api.Factory.LogFactory import LogFactory

logger = LogFactory().get_logger()


@main.route('/api')
def index():
    """默认的Get请求"""
    logger.info('')
    logger.info('---------收到index页面请求：/api----------')

    request_date = datetime.today().strftime("%Y-%m-%d")
    logger.info('---------index页面请求处理完毕-----------')
    return render_template("index.html", title='api List', date=request_date, dept_name='支行营业室',
                           admin_password="159357")


@main.route('/api/submit', methods=['POST'])
def create_performance():
    """POST方法，用于提交业绩"""
    logger.info('')
    logger.info('---------收到来POST请求：/api/submit----------')

    if not request.json or 'dept_id' not in request.json:
        # 如果请求里面没有JSON数据，或者在JSON数据里面dept_id的内容是空的
        logger.info("传入参数错误！")
        return "args_missing", 500
    if 'user_name' in request.json:
        user_name = request.json["user_name"]
    else:
        user_name = "admin"
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
            logger.info('POST请求/api/submit处理完毕，返回值%s' % "success")
            return "success", 201  # 并返回这个添加的task内容，和状态码
        else:
            logger.info('POST请求/api/submit处理完毕，返回值%s' % "fail")
            return "fail", 500


@main.route('/api/update_field', methods=['POST'])
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


@main.route('/api/send_daily_email', methods=['POST'])
def send_daily_email():
    """POST方法，用于给字段排序"""
    logger.info('')
    logger.info('---------收到POST请求：/api/send_daily_email----------')

    if not request.json or 'date' not in request.json:
        logger.info("传入参数错误！")
        return "args_missing", 500
    if 'user_name' in request.json:
        user_name = request.json["user_name"]
    else:
        user_name = "admin"
    logger.info('用户[%s]发送当日统计邮件：' % user_name)
    logger.info("data: date=%s" % request.json["date"])

    result = False
    try:
        service = EmailService()
        result = service.send_daily_email(request.json["date"])
    except Exception as e:
        logger.error('发生错误!')
        logger.error(e)
    finally:
        if result:
            logger.info('POST请求/api/send_daily_email处理完毕，返回值%s' % "success")
            return "success", 201
        else:
            logger.info('POST请求/api/send_daily_email处理完毕，返回值%s' % "fail")
            return "fail", 500


@main.route('/api/check', methods=['GET'])
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
def get_fields():
    """GET，用于获取所有字段"""
    logger.info('')
    logger.info('---------收到GET请求：/api/fields----------')
    if request.args.get('user_name') is not None:
        user_name = request.args.get('user_name')
    else:
        user_name = "admin"
    logger.info('用户[%s]修改字段：' % user_name)
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
def get_available_fields_name():
    """GET，用于获取所有可用字段"""
    logger.info('')
    logger.info('---------收到GET请求：/api/fields_name----------')
    if request.args.get('user_name') is not None:
        user_name = request.args.get('user_name')
    else:
        user_name = "admin"
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


@main.route('/api/display', methods=['GET'])
def display():
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
