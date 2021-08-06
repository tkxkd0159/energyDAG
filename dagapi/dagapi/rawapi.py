import json
from json import dumps
from flask import Blueprint, request, jsonify, redirect, render_template, g
from flask_restful import Resource, Api, abort
from webargs.flaskparser import use_args


from dagapi.auth import login_required
from dagapi.rest_schema import TxSchema
from dagapi.db import load_dag

from kudag.param import PEERS
from kudag.dag import TX
import kudag.network as net

rawapi = Blueprint('rawapi', __name__, url_prefix='/api')
rapi = Api(rawapi)

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

@rawapi.route('/genesis', methods=['GET'])
def make_genesis():
    if request.method == "GET":
        load_dag()
        data = g.dag.start_genesis()
        for id, value in data["accounts"].items():
            tx = TX(from_="genesis", to_=id, data={"value": value})
            tx_id, tx_str = g.dag.add_tx(tx, genesis=True)
            print(tx_id, tx_str, flush=True)

    return redirect(rapi.url_for(DAG_API))


@rawapi.route('/states')
def get_state():
    load_dag()
    temp = {}

    for key, value in g.dagsdb:
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

        tx = TX(from_=from_, to_=to_, data={"value": value_})
        if g.dag.validate_tx(tx, g.wallet):
            try:
                tx_id, tx_str = g.dag.add_tx(tx)
                print(f"{tx_id} is deployed", flush=True)
                net.broadcast(dumps({tx_id: tx_str}))
            except TypeError as e:
                print(e)
                print("Sender or Receiver info is not correct", flush=True)
            except UnboundLocalError:
                print("Your state DB is locking", flush=True)
        return redirect(rapi.url_for(DAG_API))


@rawapi.route('/extx', methods=['POST'])
def get_tx_from_external():
    if request.method == "POST":
        load_dag()
        req =  [v for v in request.json.values()]
        tx = TX().deserialize(req[0])
        if g.dag.validate_tx(tx, external=True):
            try:
                tx_id, tx_str = g.dag.add_tx(tx)
                # net.broadcast(dumps({tx_id: tx_str}))
            except TypeError as e:
                print(e)
                print("Sender or Receiver info is not correct", flush=True)
            except UnboundLocalError:
                print("Your state DB is locking", flush=True)
        return jsonify(req)