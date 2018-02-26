"""request api"""

from os import abort
from datetime import datetime
from flask import request
from flask import render_template

from app.api.Service.ConfigService import ConfigService
from app.api.Service.DeptInfoService import DeptInfoService
from app.api.Service.EmailService import EmailService
from app.api.Service.FieldsInfoService import FieldsInfoService
from app.api.Service.PerformanceService import PerformanceService
from app.api.Factory.LogFactory import LogFactory
from . import main

logger = LogFactory().get_logger()


@main.route('/api')
@main.route('/api/index')
def index():
    """默认的Get请求"""
    logger.info('')
    logger.info('---------收到index页面请求：/api----------')

    request_date = datetime.today().strftime("%Y-%m-%d")
    logger.info('---------index页面请求处理完毕-----------')
    return render_template("index.html", title='api List', date=request_date, dept_name='支行营业室')


@main.route('/api/submit', methods=['POST'])
def create_performance():
    """POST方法，用于提交业绩"""
    logger.info('')
    logger.info('---------收到POST请求：/api/submit----------')

    if not request.json or 'dept_id' not in request.json:
        # 如果请求里面没有JSON数据，或者在JSON数据里面dept_id的内容是空的
        abort(404)  # 返回404报错
    logger.info("args: " + str(request.json))

    service = PerformanceService()
    result = service.submit_performance(request.json)
    logger.info('---------POST请求处理完毕-----------')
    if result:
        return str(request.json['dept_id']), 201  # 并返回这个添加的task内容，和状态码
    else:
        return str(request.json['dept_id']), 500


@main.route('/api/update_field', methods=['POST'])
def update_field():
    """POST方法，用于更新字段"""
    logger.info('')
    logger.info('---------收到POST请求：/api/update_field----------')

    if not request.json or 'field_id' not in request.json:
        abort(404)
    logger.info("args: " + str(request.json))

    service = FieldsInfoService()
    result = service.update_field(request.json)
    logger.info('---------POST请求处理完毕-----------')
    if result:
        return str(request.json['field_id']), 201
    else:
        return str(request.json['field_id']), 500


@main.route('/api/create_field', methods=['POST'])
def create_field():
    """POST方法，用于更新字段"""
    logger.info('')
    logger.info('---------收到POST请求：/api/create_field----------')

    if not request.json or 'field_name' not in request.json:
        abort(404)
    logger.info("args: " + str(request.json))

    service = FieldsInfoService()
    result = service.create_field(request.json)
    logger.info('---------POST请求处理完毕-----------')
    if result:
        return str(request.json['field_name']), 201
    else:
        return str(request.json['field_name']), 500


@main.route('/api/sort_field', methods=['POST'])
def sort_field():
    """POST方法，用于给字段排序"""
    logger.info('')
    logger.info('---------收到POST请求：/api/sort_field----------')

    if not request.json or 'new_order' not in request.json:
        abort(404)
    logger.info("args: " + str(request.json))

    service = FieldsInfoService()
    result = service.sort_field(request.json)
    logger.info('---------POST请求处理完毕-----------')
    if result:
        return "", 201
    else:
        return "", 500


@main.route('/api/send_daily_email', methods=['POST'])
def send_daily_email():
    """POST方法，用于给字段排序"""
    logger.info('')
    logger.info('---------收到POST请求：/api/send_daily_email----------')

    if not request.json or 'date' not in request.json:
        abort(404)
        pass
    logger.info("Data:" + str(request.json))

    service = EmailService()
    result = service.send_daily_email(request.json["date"])
    logger.info('---------POST请求处理完毕-----------')
    if result:
        return "", 201
    else:
        return "", 500


@main.route('/api/check', methods=['GET'])
def check_submit():
    """GET，用于检查未提交业绩的网点"""
    logger.info('')
    logger.info('---------收到GET请求：/api/check----------')

    if not request.args.get('date'):
        request_date = datetime.today().strftime("%Y-%m-%d")
    else:
        request_date = request.args.get('date')
    logger.info("args: date=" + request_date)

    date = datetime.strptime(request_date, "%Y-%m-%d")
    performance_service = PerformanceService()
    check_result = performance_service.check_submission(date)
    logger.info('---------GET请求处理完毕-----------')
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
    logger.info("args: branch_name=wangjing")

    dept_info_service = DeptInfoService()
    branch_list = dept_info_service.find_branch_list(branch_name)
    logger.info('---------GET请求处理完毕-----------')
    return branch_list, 201


@main.route('/api/fields', methods=['GET'])
def get_fields():
    """GET，用于获取所有字段"""
    logger.info('')
    logger.info('---------收到GET请求：/api/fields----------')

    fields_info_service = FieldsInfoService()
    fields_list = fields_info_service.find_fields_list()
    logger.info('---------GET请求处理完毕-----------')
    return fields_list, 201


@main.route('/api/fields_name', methods=['GET'])
def get_available_fields_name():
    """GET，用于获取所有可用字段"""
    logger.info('')
    logger.info('---------收到GET请求：/api/fields_name----------')

    fields_info_service = FieldsInfoService()
    fields_list = fields_info_service.find_available_fields_name()
    logger.info('---------GET请求处理完毕-----------')
    return fields_list, 201


@main.route('/api/display', methods=['GET'])
def display():
    """GET，用于检查未提交业绩的网点"""
    logger.info('')
    logger.info('---------收到GET请求：/api/display----------')

    if not request.args.get('date'):
        request_date = datetime.today().strftime("%Y-%m-%d")
    else:
        request_date = request.args.get('date')

    if not request.args.get('dept_name'):
        return "", 201
    else:
        request_dept_name = request.args.get('dept_name')
    logger.info("args: date=" + request.args.get('date') + ", dept_name=" + request.args.get('dept_name'))

    date = datetime.strptime(request_date, "%Y-%m-%d")
    performance_service = PerformanceService()
    performance = performance_service.display(date, request_dept_name)
    logger.info('---------GET请求处理完毕-----------')
    return performance, 201


@main.route('/api/admin', methods=['GET'])
def admin():
    """GET，用于检查管理员密码是否正确"""
    logger.info('')
    logger.info('---------收到GET请求：/api/admin----------')

    logger.info(request.args)
    admin_password = ""
    if not request.args.get('admin_password'):
        abort(404)
    else:
        admin_password = request.args.get('admin_password')
    logger.info("args: admin_password=" + admin_password)

    config_service = ConfigService()
    result = config_service.check_password(admin_password)
    logger.info('密码验证结果：' + result)
    logger.info('---------GET请求处理完毕-----------')
    if result:
        return "access", 201
    else:
        return "forbid", 201
