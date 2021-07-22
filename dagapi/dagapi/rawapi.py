import requests
from json import dumps
from flask import Blueprint, request, jsonify, session, redirect, render_template, g
from flask_restful import Resource, Api, abort
from webargs.flaskparser import use_args


from dagapi.auth import login_required
from dagapi.rest_schema import TxSchema

from kudag import MY_DB, MY_SDB
from kudag.param import PEERS
from kudag.dag import TX, DAG
from kudag.wallet import Wallet
import kudag.network

DATA = {"action": "minus"}
Jheader = {'Content-Type': 'application/json'}

rawapi = Blueprint('rawapi', __name__, url_prefix='/api')
rapi = Api(rawapi)

my_dag = DAG(MY_DB, MY_SDB)
my_dag.load_dag()


def abort_if_dag_not_exist():
    if my_dag.txs == {}:
        abort(404, message="DAG doesn't exist")
def abort_if_tx_not_exist(txid: str):
    if txid not in my_dag.txs:
        abort(404, message=f"TXID << {txid} >> doesn't exist")

@rawapi.route('/', methods=('GET', 'POST'))
def index():
    if request.method == "GET":
        return "\nHello I am DAG API\n"


@rawapi.route('/states')
def get_state():
    import json
    temp = {}
    with MY_DB.snapshot() as sn:
        for key, value in sn:
            temp[key.decode()] = json.loads(value.decode())
    return temp


# TODO : request call after get broadcasting tx
@rawapi.route('/broadcast', methods=['GET', 'POST'])
def broadcast():
    if request.method == "GET":
        for i in PEERS:
            r = requests.post(url=i, headers=Jheader, data=dumps(DATA))
            print(r.text, flush=True)

        return "Success Broadcasting\n"

    elif request.method == "POST":
        req = request.json
        return req

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
        if txid == 0:
            abort_if_dag_not_exist()
            return my_dag.txs
        else:
            abort_if_tx_not_exist(txid)
            return my_dag.txs[txid]

    @use_args(TxSchema())
    def post(self, args):
        my_dag.txs[args["id"]] = args
        return 200
rapi.add_resource(DAG_API, '/dag', '/dag/<txid>', endpoint='dag')

@rawapi.route('/tx', methods=['GET', 'POST'])
@login_required
def tx_interface():
    if request.method == "GET":
        # my_pwhash = session.get("pwhash")
        # mywallet = Wallet(pwhash=my_pwhash)
        # mywallet.init()
        addr_list = []
        mywallet = g.wallet
        for i in range(mywallet.key_nums):
            addr_list.append((i, mywallet.addr[str(i)]))
        return render_template('tx.html', addrs=addr_list)
    elif request.method == "POST":
        req = request.form
        from_ = req['from-category']
        to_ = req['to_']
        value_ = req['value_']
        contract_code = req['CC']

        target_tx = TX(from_=from_, to_=to_, data={"value": value_})
        if my_dag.validate_tx(target_tx, g.wallet):
            tx_id, _ = my_dag.add_tx(target_tx)
            # print(f'TX ID : {tx_id}', flush=True)
        return redirect(rapi.url_for(DAG_API))


@rawapi.route('/extx', methods=['POST'])
def get_tx_from_external():
    pass