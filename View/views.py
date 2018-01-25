from os import abort

from flask import request, jsonify
from requests import auth

from APP import APP

tasks =[
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
    return "Hello, World!"


@APP.route('/api/v1.0/tasks/<int:task_id>',methods=['GET'])
def get_task(task_id):
    task = list(filter(lambda t : t['id'] == task_id ))   #检查tasks内部元素，是否有元素的id的值和参数id相匹配
    if len(task) == 0:                                       #有的话，就返回列表形式包裹的这个元素，如果没有，则报错404
        abort(404)
    return jsonify({'tasks':task[0]})


@APP.route('/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or 'dept_name' not in request.json:  # 如果请求里面没有JSON数据，或者在JSON数据里面，title的内容是空的
        abort(404)  # 返回404报错

    return request.json['dept_name'], 201  # 并返回这个添加的task内容，和状态码


@APP.route('/api/v1.0/tasks/<int:task_id>', methods = ['PUT'])
@auth.login_required
def update_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify( { 'task': make_public_task(task[0]) } )
