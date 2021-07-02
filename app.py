import sys
from pathlib import Path
from flask import Flask, request, render_template, escape, redirect
from flask_cors import CORS
from flask_restful import Resource, Api, abort
from webargs.flaskparser import use_args

from kudag.dag import TxHash, TX
from kudag import MY_DAG, MY_DB
from rest_schema import TxSchema

from front import front
from auth import auth, login_required
from rdb import init_dbapp


RDB_PATH = Path.cwd().joinpath('sqlite3')
if not RDB_PATH.exists():
    RDB_PATH.mkdir(parents=True)


##################################################
app = Flask(__name__)
CORS(app)
app.config.from_mapping(
    SECRET_KEY='TPdlwotmd4aLWRbyVq8zu9v82dWYW1',
    UPLOAD_FOLDER='./download',
    DATABASE=str(RDB_PATH.joinpath('kudag_user.db')),
    )

app.register_blueprint(front)
app.register_blueprint(auth)

from rdb import init_dbapp
init_dbapp(app)

api = Api(app)


@app.errorhandler(404)
def page_not_found(e):
    # jsonify(error=str(e)).get_data()  -> {"error":"404 Not Found: Resource not found"}
    return render_template('404.html'), 404

def abort_if_dag_not_exist():
    if MY_DAG.txs == {}:
        abort(404, message="DAG doesn't exist")

def abort_if_tx_not_exist(txid: TxHash):
    if txid not in MY_DAG.txs:
        abort(404, message=f"TXID << {txid} >> doesn't exist")


# Use @app.route
@app.route('/', methods=['GET'])
def index():
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
@login_required
def tx_interface():
    if request.method == "GET":
        return render_template('tx.html')

    elif request.method == "POST":
        req = request.form

        from_ = req['from_']
        to_ = req['to_']
        value_ = req['value_']

        target_tx = TX(from_=from_, to_=to_, data={"value": value_})
        tx_id, _ = MY_DAG.add_tx(target_tx)
        print(f'TX ID : {tx_id}', file=sys.stderr)
        return redirect("http://127.0.0.1:5000/dag")


##################################################################

@app.route('/get_state')
def get_state():
    import json
    temp = {}
    with MY_DB.snapshot() as sn:
        for key, value in sn:
            temp[key.decode()] = json.loads(value.decode())

    return temp


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    import sys
    # print(type(subpath), file=sys.stdout)
    return f'Subpath {escape(subpath)}'




"""
*    curl http://localhost:5000/todos
*    curl http://localhost:5000/todos/todo2 -X DELETE -v // Delete a task
*    curl http://localhost:5000/todos -d "task=something new" -v   // Add new task(POST), args['task'] = 'something new'
*    curl http://localhost:5000/todos/todo3 -d "task=something different" -X PUT -v // Update a task
*    curl -d @test_rest.json -H "Content-Type: application/json" -X POST http://localhost:5000/profile
"""