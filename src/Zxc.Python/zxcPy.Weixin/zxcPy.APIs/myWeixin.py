# -*- coding: utf-8 -*-
"""
Created on  张斌 2017-11-19 14:40:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Rest API Weixin网页版接口操作() --测试用
"""
import os  
from flask import Flask
from flask_restful import reqparse, Api, Resource
import myWeb


#Weixin消息发送(API接口)  
class Send_Msg(Resource):
    def get(self, usrName, msgInfo, mstType = "TEXT"): 
        return "This is myWeixin_API's Test web page..."
        return TODOS
    
#测试(API方法)  
class TestAPI2(Resource):
    def get(self, param):
        strReturn = "参数：" + param
        return strReturn
    
    def get2(self, param):
        strReturn = "参数2：" + param
        return strReturn
 

#定义全局参数（复杂API）
TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '哈哈哈3a'},
    'todo3': {'task': 'profit!'},
}
parser = reqparse.RequestParser()
parser.add_argument('task')


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self): 
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201


#测试API入口
def Add_API(api, app): 
    api.add_resource(TestAPI, '/test')
    api.add_resource(TestAPI2, '/test/<param>')
    api.add_resource(TodoList, '/todos')
    api.add_resource(Todo, '/todos/<todo_id>')

    
    #添加一个页面(普通页面)
    @app.route('/HelloWorld')
    def hello_world():
        return "Hello World......!" 
