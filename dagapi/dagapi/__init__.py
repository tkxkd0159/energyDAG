import sys
from pathlib import Path
from flask import Flask, request, session, render_template, escape, redirect
from flask_cors import CORS
from flask_restful import Resource, Api, abort
from webargs.flaskparser import use_args

from kudag.dag import TxHash, TX
from kudag.wallet import Wallet
from kudag import MY_DAG, MY_DB

from dagapi.rest_schema import TxSchema
from dagapi.auth import login_required

def create_app(test_config=None):
    base_path = Path(__file__).parents[2]
    rdb_path = base_path.joinpath('sqlite3')
    if not rdb_path.exists():
        rdb_path.mkdir(parents=True)

    ##################################################
    app = Flask(__name__)
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY='TPdlwotmd4aLWRbyVq8zu9v82dWYW1',
        UPLOAD_FOLDER=str(base_path.joinpath('download')),
        DATABASE=str(rdb_path.joinpath('kudag_user.db')),
        )

    from dagapi.rdb import init_dbapp
    init_dbapp(app)

    from dagapi.front import front
    from dagapi.auth import auth
    app.register_blueprint(front)
    app.register_blueprint(auth)


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
            my_pwhash = session.get("pwhash")
            mywallet = Wallet(pwhash=my_pwhash)
            mywallet.init()
            addr_list = []
            for i in range(mywallet.key_nums):
                addr_list.append((i, mywallet.addr[str(i)]))

            return render_template('tx.html', addrs=addr_list)

        elif request.method == "POST":
            req = request.form

            from_ = req['from-category']
            to_ = req['to_']
            value_ = req['value_']
            contract_code = req['CC']
            print(from_, to_, value_, contract_code, file=sys.stdout)

            target_tx = TX(from_=from_, to_=to_, data={"value": value_})
            tx_id, _ = MY_DAG.add_tx(target_tx)
            # print(f'TX ID : {tx_id}', file=sys.stderr)
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
        # print(subpath, file=sys.stdout)
        return f'Subpath {escape(subpath)}'

    return app




    """
    *    curl http://localhost:5000/todos
    *    curl http://localhost:5000/todos/todo2 -X DELETE -v // Delete a task
    *    curl http://localhost:5000/todos -d "task=something new" -v   // Add new task(POST), args['task'] = 'something new'
    *    curl http://localhost:5000/todos/todo3 -d "task=something different" -X PUT -v // Update a task
    *    curl -d @test_rest.json -H "Content-Type: application/json" -X POST http://localhost:5000/profile
    """