import sqlite3
import click
from flask import current_app
from flask import g
from flask.cli import with_appcontext

from kudag.db import init_db, init_state_db
from kudag.param import HTTP_PORT
from kudag.dag import DAG

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

def close_all_dag_db(e=None):
    db = g.pop("dagdb", None)
    sdb = g.pop("dagsdb", None)
    if db is not None:
        db.close()
    if sdb is not None:
        sdb.close()

def get_rdb():
    if "rdb" not in g:
        g.rdb = sqlite3.connect(current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES)
        g.rdb.row_factory = sqlite3.Row

    return g.rdb


def close_rdb(e=None):
    db = g.pop("rdb", None)
    if db is not None:
        db.close()


def init_rdb():
    db = get_rdb()
    with current_app.open_resource("initrdb.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
@with_appcontext
def init_rdb_command():
    init_rdb()
    click.echo("Initialized the database.")


def init_dbapp(app):
    app.teardown_appcontext(close_rdb)
    app.cli.add_command(init_rdb_command)