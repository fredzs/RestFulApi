'''
request api

'''


from os import abort
from flask import request
from APP import APP

tasks = [
    {
        'dept_name': 1,
        'date': '2018-01-01',
        'project_1': 100,
        'project_2': 'Cheese',
        'project_3': 'Pizza',
        'project_4': 'Fruit',
        'project_5': 'Tylenol'
    },
    {
        'dept_name': 1,
        'date': '2018-02-01',
        'project_1': 200,
        'project_2': 'Apple',
        'project_3': 'Banana',
        'project_4': 'Orange',
        'project_5': 'Pear'
    }]


@APP.route('/')
@APP.route('/index')
def index():
    '''默认的Get请求'''
    return "Hello, World!"


@APP.route('/api/tasks', methods=['POST'])
def create_task():
    '''POST方法用于测试'''
    print(request.json)
    if not request.json or 'dept_name' not in request.json:
        # 如果请求里面没有JSON数据，或者在JSON数据里面，title的内容是空的
        abort(404)  # 返回404报错

    return request.json['dept_name'], 201  # 并返回这个添加的task内容，和状态码
