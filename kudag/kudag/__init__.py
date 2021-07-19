# pip install -e .
from kudag.db import init_db
from kudag.dag import DAG

try:
    MY_DB = init_db()
    MY_DAG = DAG(MY_DB)
    MY_DAG.load_dag()
except:
    pass
