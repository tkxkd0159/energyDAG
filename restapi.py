from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse



app = Flask(__name__)

## Use @app.route

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/user/<user_name>') # URL뒤에 <>을 이용해 가변 경로를 적는다
def hello_user(user_name):
    return f'Hello, {user_name}'


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






from webargs import fields
from webargs.flaskparser import use_args


USERS = {"user1":{'id':0, 'username':"PMS", 'lang':['python', 'java']}}

user_args = {
    "username": fields.Str(required=True), # Required arguments
    "password": fields.Str(validate=lambda p: len(p) >= 6),  # Validation
    "lang": fields.List(fields.Str()),
    "display_per_page": fields.Int(missing=10),  # Default value when argument is missing
    "user_type": fields.Str(data_key="user-type") # rename a key "user-type" for safety
}

@app.route("/profiles", methods=["GET"])
@app.route("/profiles/", methods=["GET", "PATCH"])
def my_profile():
    if request.method == "GET":
        return USERS

@app.route("/profile", methods=["POST"])
@use_args(user_args)
def post_profile(args):
    if request.method == "POST":
        user_id = int(max(USERS.keys()).lstrip('user')) + 1
        USERS[f'user{user_id}'] = {'id':user_id, 'username':args['username'], 'lang':args['lang']}
        return USERS[f'user{user_id}'], 200

from marshmallow import Schema, fields
from datetime import datetime

class User:
    def __init__(self, username, password, lang):
        self.username = username
        self.password = password
        self.lang = lang
        self.created = datetime.now()

class UserSchema(Schema):
    id = fields.Int(dump_only=True)       # read-only
    username = fields.Str(required=True)
    password = fields.Str(load_only=True, data_key="my-password") # write-only
    lang = fields.List(fields.Str())
    created = fields.DateTime(dump_only=True)

user1 = User("LJS", "myrandompasswd", lang=["python", "java"])
res = UserSchema().dump(user1)
temp_id = int(max(USERS.keys()).lstrip('user')) + 1
USERS[f'user{temp_id}'] = res

class UserDB(Resource):
    def get(self):
        return USERS

    @use_args(UserSchema())
    def post(self, args):   # data deserilization
        d = datetime.now().isoformat(timespec="minutes")
        myid = int(max(USERS.keys()).lstrip('user')) + 1
        USERS[f'user{myid}'] =  {'id':myid, 'username':args['username'], 'my password':args['password'], 'lang':args['lang'], 'created':d}
        return 200

api.add_resource(UserDB, '/users') # URL Router에 mapping



if __name__ == "__main__":
    app.run(debug=True)



"""
*    curl http://localhost:5000/todos
*    curl http://localhost:5000/todos/todo2 -X DELETE -v // Delete a task
*    curl http://localhost:5000/todos -d "task=something new" -v   // Add new task(POST), args['task'] = 'something new'
*    curl http://localhost:5000/todos/todo3 -d "task=something different" -X PUT -v // Update a task
*    curl -d @test_rest.json -H "Content-Type: application/json" -X POST http://localhost:5000/profile
"""