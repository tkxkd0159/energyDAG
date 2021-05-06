from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse

from lib import param


app = Flask(__name__)
api = Api(app)

## Use @app.route

@app.route('/')
def hello_world():
    return 'Hello, World!'


# TODO : replace legacy parser to use_args (Schema)
parser2 = reqparse.RequestParser()
parser2.add_argument('ver')
parser2.add_argument('timestamp')

class DAG_API(Resource):
    def get(self):
        return param.MYDAG

    def post(self):
        args = parser2.parse_args()
        param.MYDAG.update(args)
        return 200


api.add_resource(DAG_API, '/dag')

if __name__ == "__main__":
    app.run(debug=True)



"""
*    curl http://localhost:5000/todos
*    curl http://localhost:5000/todos/todo2 -X DELETE -v // Delete a task
*    curl http://localhost:5000/todos -d "task=something new" -v   // Add new task(POST), args['task'] = 'something new'
*    curl http://localhost:5000/todos/todo3 -d "task=something different" -X PUT -v // Update a task
*    curl -d @test_rest.json -H "Content-Type: application/json" -X POST http://localhost:5000/profile
"""