from flask import Flask
from flask_restful import Resource, Api, abort, reqparse


app = Flask(__name__)

## Use @app.route

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/user/<user_name>') # URL뒤에 <>을 이용해 가변 경로를 적는다
def hello_user(user_name):
    return f'Hello, {user_name}'

def test_url():
    return f'Hello test  url', 200
app.add_url_rule('/testall/ljs', 'test_url', test_url)

## Use flask Api
api = Api(app)

TODOS = {
    'todo1': {'task': 'Make Money'},
    'todo2': {'task': 'Play PS4'},
    'todo3': {'task': 'Study!'},
}

#예외 처리
def not_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')


class Todo(Resource):
    def get(self, todo_id):
        not_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        not_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201

api.add_resource(Todo, '/todos/<todo_id>') # URL Router에 mapping


class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = f'todo{todo_id}'
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 200

api.add_resource(TodoList, '/todos', '/todos/') # URL Router에 mapping




if __name__ == "__main__":
    app.run(debug=True)


"""
*    curl http://localhost:5000/todos
*    curl http://localhost:5000/todos/todo2 -X DELETE -v // Delete a task
*    curl http://localhost:5000/todos -d "task=something new" -v   // Add new task(POST), args['task'] = 'something new'
*    curl http://localhost:5000/todos/todo3 -d "task=something different" -X PUT -v // Update a task
"""