from flask import Flask
from flask_restful import Resource, Api, abort, reqparse

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('task')

TODOs = {
    1: {'task': 'dictionary??'},
    2: {'task': 'what do not buy them'},
    3: {'task': 'throw a fit'},
}

def abort_if_todo_not_found(todo_id):
    if todo_id not in TODOs:
        abort(404, message="TODO {} does not exist".format(todo_id))

def add_todo(todo_id):
    args = parser.parse_args()
    todo = {'task': args['task']}
    TODOs[todo_id] = todo
    return todo

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_not_found(todo_id)
        return TODOs[todo_id]
    def delete(self, todo_id):
        abort_if_todo_not_found(todo_id)
        del TODOs[todo_id]
        return '', 204

    def put(self, todo_id):
        return add_todo(todo_id), 201

class TodoList(Resource):
    def get(self):
        return TODOs

    def post(self):
        todo_id = max(TODOs.keys()) + 1
        return add_todo(todo_id), 201

api.add_resource(Todo, '/todos/<int:todo_id>')
api.add_resource(TodoList, '/todos')


def hello():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)
