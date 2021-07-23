import json
from json import dumps
from flask import Blueprint, request, jsonify, redirect, render_template, g
from flask_restful import Resource, Api, abort
from webargs.flaskparser import use_args


from dagapi.auth import login_required
from dagapi.rest_schema import TxSchema

from kudag.param import PEERS, HTTP_PORT
from kudag.dag import TX, DAG
import kudag.network as net
from kudag.db import init_db, init_state_db

rawapi = Blueprint('rawapi', __name__, url_prefix='/api')
rapi = Api(rawapi)

def load_dagdb():
    if "dagdb" not in g:
        g.dagdb = init_db(HTTP_PORT)

def load_dagsdb():
    if "dagsdb"  not in g:
        g.dagsdb = init_state_db(HTTP_PORT)

def load_dag():

    load_dagdb()
    load_dagsdb()
    if "dag" not in g:
        g.dag = DAG(g.dagdb, g.dagsdb)
        g.dag.load_dag()

def close_dag(e=None):
    db = g.pop("dagdb", None)
    sdb = g.pop("dagsdb", None)
    if db is not None:
        db.close()
    if sdb is not None:
        sdb.close()

def abort_if_dag_not_exist():
    if g.dag.txs == {}:
        abort(404, message="DAG doesn't exist")
def abort_if_tx_not_exist(txid: str):
    if txid not in g.dag.txs:
        abort(404, message=f"TXID << {txid} >> doesn't exist")

@rawapi.route('/', methods=('GET', 'POST'))
def index():
    if request.method == "GET":
        return "\nHello I am DAG API\n"


@rawapi.route('/states')
def get_state():
    load_dagsdb()
    temp = {}
    with g.dagsdb.snapshot() as sn:
        for key, value in sn:
            temp[key.decode()] = json.loads(value.decode())
    return temp

@rawapi.route('/peers', methods=['GET', 'POST'])
def handle_peer():
    if request.method == "GET":

        return jsonify({"peers":list(PEERS)})

    elif request.method == "POST":
        req = request.json
        for peer in req['peers2']:
            PEERS.add(peer)

        return jsonify({"peers":list(PEERS)})

class DAG_API(Resource):
    def get(self, txid=0):
        load_dag()
        if txid == 0:
            abort_if_dag_not_exist()
            return g.dag.txs
        else:
            abort_if_tx_not_exist(txid)
            return g.dag.txs[txid]

    @use_args(TxSchema())
    def post(self, args):
        load_dag()
        g.dag.txs[args["id"]] = args
        return 200
rapi.add_resource(DAG_API, '/dag', '/dag/<txid>', endpoint='dag')

@rawapi.route('/tx', methods=['GET', 'POST'])
@login_required
def tx_interface():
    if request.method == "GET":
        addr_list = []
        mywallet = g.wallet
        for i in range(mywallet.key_nums):
            addr_list.append((i, mywallet.addr[str(i)]))
        return render_template('tx.html', addrs=addr_list)
    elif request.method == "POST":
        load_dag()
        req = request.form
        from_ = req['from-category']
        to_ = req['to_']
        value_ = req['value_']
        contract_code = req['CC']

        target_tx = TX(from_=from_, to_=to_, data={"value": value_})
        if g.dag.validate_tx(target_tx, g.wallet):
            tx_id, tx_str = g.dag.add_tx(target_tx)
            net.broadcast(dumps({tx_id: tx_str}))
            # print(f'TX ID : {tx_id}', flush=True)
        return redirect(rapi.url_for(DAG_API))


@rawapi.route('/extx', methods=['POST'])
def get_tx_from_external():
    pass