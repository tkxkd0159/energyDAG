from pathlib import Path
from flask import Flask, request, render_template, escape
from flask_cors import CORS


from kudag.param import HTTP_PORT


def page_not_found(e):
    # jsonify(error=str(e)).get_data()  -> {"error":"404 Not Found: Resource not found"}
    return render_template("404.html"), 404


def create_app(test_config=None):
    base_path = Path(__file__).parents[2]
    rdb_path = base_path.joinpath("sqlite3", HTTP_PORT)
    if not rdb_path.exists():
        rdb_path.mkdir(parents=True)
    ##################################################
    app = Flask(__name__)
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY="TPdlwotmd4aLWRbyVq8zu9v82dWYW1",
        UPLOAD_FOLDER=str(base_path.joinpath("download")),
        DATABASE=str(rdb_path.joinpath("kudag_user.db")),
    )
    from dagapi.db import init_dbapp, close_all_dag_db

    init_dbapp(app)
    app.teardown_appcontext(close_all_dag_db)
    app.register_error_handler(404, page_not_found)

    from dagapi.front import front
    from dagapi.auth import auth
    from dagapi.rawapi import rawapi

    app.register_blueprint(front)
    app.register_blueprint(auth)
    app.register_blueprint(rawapi)

    @app.route("/", methods=["GET"])
    def index():
        if request.method == "GET":
            return render_template("index.html")

    @app.route("/shutdown", methods=["GET"])
    def shutdown():
        def shutdown_server():
            func = request.environ.get("werkzeug.server.shutdown")
            if func is None:
                raise RuntimeError("Not running with the Werkzeug Server")
            func()

        shutdown_server()
        return "Server shutting down..."

    ##################################################################

    @app.route("/path/<path:subpath>")
    def show_subpath(subpath):
        # print(subpath, file=sys.stdout)
        return f"Subpath {escape(subpath)}"

    return app


"""
    *    curl http://localhost:5000/todos
    *    curl http://localhost:5000/todos/todo2 -X DELETE -v // Delete a task
    *    curl http://localhost:5000/todos -d "task=something new" -v   // Add new task(POST), args['task'] = 'something new'
    *    curl http://localhost:5000/todos/todo3 -d "task=something different" -X PUT -v // Update a task
    *    curl -d @test_rest.json -H "Content-Type: application/json" -X POST http://localhost:5000/profile
"""
