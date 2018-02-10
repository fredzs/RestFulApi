"""request api"""

import logging
from os import abort
from datetime import datetime
from flask import request
from app.api.Service.DeptInfoService import DeptInfoService
from app.api.Service.FieldsInfoService import FieldsInfoService
from app.api.Service.PerformanceService import PerformanceService
from . import main


logger = logging.getLogger()


@main.route('/')
@main.route('/index')
def index():
    """默认的Get请求"""
    return "Hello, World!"


@main.route('/api/submit', methods=['POST'])
def create_performance():
    """POST方法，用于提交业绩"""
    logger.info(request.json)
    if not request.json or 'dept_id' not in request.json:
        # 如果请求里面没有JSON数据，或者在JSON数据里面，title的内容是空的
        abort(404)  # 返回404报错
    logger.info('---------收到POST请求：/api/submit----------')
    service = PerformanceService()
    performance = PerformanceService.read_json(request.json)
    result = service.submit_performance(performance)
    logger.info('---------POST请求处理完毕-----------')
    if result:
        return str(request.json['dept_id']), 201  # 并返回这个添加的task内容，和状态码
    else:
        return str(request.json['dept_id']), 500


@main.route('/api/update_field', methods=['POST'])
def update_field():
    """POST方法，用于更新字段"""
    logger.info(request.json)
    if not request.json or 'field_id' not in request.json:
        # 如果请求里面没有JSON数据，或者在JSON数据里面，title的内容是空的
        abort(404)  # 返回404报错
    logger.info('---------收到POST请求：/api/update_field----------')
    service = FieldsInfoService()
    result = service.update_field(request.json)
    logger.info('---------POST请求处理完毕-----------')
    if result:
        return str(request.json['field_id']), 201  # 并返回这个添加的task内容，和状态码
    else:
        return str(request.json['field_id']), 500


@main.route('/api/check', methods=['GET'])
def check_submit():
    """GET，用于检查未提交业绩的网点"""
    logger.info('---------收到GET请求：/api/check----------')
    if not request.args.get('date'):
        request_date = datetime.today().strftime("%Y-%m-%d")
    else:
        request_date = request.args.get('date')
    date = datetime.strptime(request_date, "%Y-%m-%d")
    performance_service = PerformanceService()
    check_result = performance_service.check_submission(date)
    logger.info('---------POST请求处理完毕-----------')

    return check_result, 201  # 并返回这个添加的task内容，和状态码


@main.route('/api/branches', methods=['GET'])
def get_branches():
    """GET，用于获取所有网点"""
    logger.info('---------收到GET请求：/api/branches----------')
    if not request.args.get('branch_name'):
        branch_name = "wangjing"
    else:
        branch_name = "wangjing"
    dept_info_service = DeptInfoService()
    branch_list = dept_info_service.find_branch_list(branch_name)
    logger.info('---------POST请求处理完毕-----------')

    return branch_list, 201  # 并返回这个添加的task内容，和状态码


@main.route('/api/fields', methods=['GET'])
def get_fields():
    """GET，用于获取所有字段"""
    logger.info('---------收到GET请求：/api/fields----------')
    fields_info_service = FieldsInfoService()
    fields_list = fields_info_service.find_fields_list()
    logger.info('---------POST请求处理完毕-----------')

    return fields_list, 201  # 并返回这个添加的task内容，和状态码


@main.route('/api/fields_name', methods=['GET'])
def get_fields_name():
    """GET，用于获取所有字段"""
    logger.info('---------收到GET请求：/api/fields_name----------')
    fields_info_service = FieldsInfoService()
    fields_list = fields_info_service.find_fields_name()
    logger.info('---------POST请求处理完毕-----------')

    return fields_list, 201  # 并返回这个添加的task内容，和状态码


@main.route('/api/display', methods=['GET'])
def display():
    """GET，用于检查未提交业绩的网点"""
    logger.info('---------收到GET请求：/api/display----------')
    if not request.args.get('date'):
        request_date = datetime.today().strftime("%Y-%m-%d")
    else:
        request_date = request.args.get('date')
    if not request.args.get('dept_name'):
        return "", 201
    else:
        request_dept_name = request.args.get('dept_name')
    date = datetime.strptime(request_date, "%Y-%m-%d")
    performance_service = PerformanceService()
    performance = performance_service.display(date, request_dept_name)
    logger.info('---------POST请求处理完毕-----------')

    return performance, 201  # 并返回这个添加的task内容，和状态码
