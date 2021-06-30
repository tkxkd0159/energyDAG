import requests
from flask import Flask, request, render_template, escape, redirect
from flask_cors import CORS
from flask_restful import Resource, Api, abort
from webargs.flaskparser import use_args

from front import front
from kudag.dag import TxHash, DAG, TX
from kudag.db import DB, STATE_DB
from rest_schema import TxSchema


# flask run

MY_DAG = DAG(DB)
MY_DAG.load_dag()

##################################################
app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = 'TPdlwotmd4aLWRbyVq8zu9v82dWYW1'
app.config['UPLOAD_FOLDER'] = './download'
app.register_blueprint(front)
api = Api(app)


def abort_if_dag_not_exist():
    if MY_DAG.txs == {}:
        abort(404, message="DAG doesn't exist")

def abort_if_tx_not_exist(txid: TxHash):
    if txid not in MY_DAG.txs:
        abort(404, message=f"TXID << {txid} >> doesn't exist")


# Use @app.route
@app.route('/', methods=['GET'])
def dag_index():
    if request.method == 'GET':
        return render_template('index.html')

# flask_restful use only for JSON
class DAG_API(Resource):

    def get(self, txid=0):
        if txid == 0:
            abort_if_dag_not_exist()
            return MY_DAG.txs
        else:
            abort_if_tx_not_exist(txid)
            return MY_DAG.txs[txid]

    @use_args(TxSchema())
    def post(self, args):
        MY_DAG.txs[args["id"]] = args

        return 200

api.add_resource(DAG_API, '/dag', '/dag/<txid>')


@app.route('/tx', methods=['GET', 'POST'])
def tx_interface():
    if request.method == "GET":
        return render_template('dag.html')

    elif request.method == "POST":
        req = request.form

        from_ = req['from_']
        to_ = req['to_']
        value_ = req['value_']

        target_tx = TX(from_=from_, to_=to_, data={"value": value_})
        _, tx = MY_DAG.add_tx(target_tx)
        requests.post(url="http://127.0.0.1:5000/dag",
                      headers={'Content-Type': 'application/json'},
                      data=tx
                     )

        return redirect("http://127.0.0.1:5000/dag")

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return f'Subpath {escape(subpath)}'




"""
*    curl http://localhost:5000/todos
*    curl http://localhost:5000/todos/todo2 -X DELETE -v // Delete a task
*    curl http://localhost:5000/todos -d "task=something new" -v   // Add new task(POST), args['task'] = 'something new'
*    curl http://localhost:5000/todos/todo3 -d "task=something different" -X PUT -v // Update a task
*    curl -d @test_rest.json -H "Content-Type: application/json" -X POST http://localhost:5000/profile
"""