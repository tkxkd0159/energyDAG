from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse
from webargs.flaskparser import use_args

from lib.param import MYDAG
from rest_schema import TxSchema

app = Flask(__name__)
api = Api(app)

## Use @app.route

@app.route('/')
def hello_world():
    return 'Hello, World!'


class DAG_API2(Resource):

    def get(self):
        return MYDAG

    @use_args(TxSchema())
    def post(self, args):
        MYDAG['test'] = args
        print(args)

        return 200

api.add_resource(DAG_API2, '/dag2')

if __name__ == "__main__":
    app.run(debug=True)



"""
*    curl http://localhost:5000/todos
*    curl http://localhost:5000/todos/todo2 -X DELETE -v // Delete a task
*    curl http://localhost:5000/todos -d "task=something new" -v   // Add new task(POST), args['task'] = 'something new'
*    curl http://localhost:5000/todos/todo3 -d "task=something different" -X PUT -v // Update a task
*    curl -d @test_rest.json -H "Content-Type: application/json" -X POST http://localhost:5000/profile
"""