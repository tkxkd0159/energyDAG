from flask import Flask, request, render_template
from flask_restful import Resource, Api, abort
from webargs.flaskparser import use_args
from front import front

from lib.param import MYDAG
from lib.dag import TXHASH
from rest_schema import TxSchema


app = Flask(__name__)
app.config["SECRET_KEY"] = 'TPdlwotmd4aLWRbyVq8zu9v82dWYW1'
app.config['UPLOAD_FOLDER'] = './download'
app.register_blueprint(front)
api = Api(app)

## Use @app.route

def abort_if_dag_not_exist():
    if MYDAG == {}:
        abort(404, message="DAG doesn't exist")

def abort_if_tx_not_exist(txid: TXHASH):
    if txid not in MYDAG:
        abort(404, message=f"TXID << {txid} >> doesn't exist")

@app.route('/', methods=['GET'])
def dag_index():
    if request.method == 'GET':
        return render_template('index.html')

class DAG_API(Resource):

    def get(self, txid=0):
        if txid == 0:
            abort_if_dag_not_exist()
            return MYDAG
        else:
            abort_if_tx_not_exist(txid)
            return MYDAG[txid]

    @use_args(TxSchema())
    def post(self, args):
        MYDAG["mytxid"] = args

        return 200

api.add_resource(DAG_API, '/dag', '/dag/<txid>')

if __name__ == "__main__":
    app.run(debug=True)



"""
*    curl http://localhost:5000/todos
*    curl http://localhost:5000/todos/todo2 -X DELETE -v // Delete a task
*    curl http://localhost:5000/todos -d "task=something new" -v   // Add new task(POST), args['task'] = 'something new'
*    curl http://localhost:5000/todos/todo3 -d "task=something different" -X PUT -v // Update a task
*    curl -d @test_rest.json -H "Content-Type: application/json" -X POST http://localhost:5000/profile
"""