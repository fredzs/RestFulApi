"""request api"""

import logging
from os import abort
from datetime import datetime
from flask import request
from APP import APP
from Service.PerformanceService import PerformanceService


@APP.route('/')
@APP.route('/index')
def index():
    """默认的Get请求"""
    return "Hello, World!"


@APP.route('/api/submit', methods=['POST'])
def create_performance():
    """POST方法，用于提交业绩"""
    logging.info(request.json)
    if not request.json or 'dept_id' not in request.json:
        # 如果请求里面没有JSON数据，或者在JSON数据里面，title的内容是空的
        abort(404)  # 返回404报错
    logging.info('---------收到POST请求：/api/submit----------')
    service = PerformanceService()
    performance = PerformanceService.read_json(request.json)
    service.submit_performance(performance)
    logging.info('---------POST请求处理完毕-----------')

    return request.json['dept_id'], 201  # 并返回这个添加的task内容，和状态码


@APP.route('/api/check', methods=['GET'])
def create_performance():
    """GET，用于检查未提交业绩的网点"""
    logging.info('---------收到GET请求：/api/check----------')
    request_date = request.args.get('date')
    date = datetime.strptime(request_date, "%Y-%m-%d")
    check_result = PerformanceService.check_submission(date)
    logging.info('---------POST请求处理完毕-----------')

    return check_result, 201  # 并返回这个添加的task内容，和状态码
