import unittest
import json

from kudag.dag import TX, DAG
from kudag.db import DB, STATE_DB


class Database(unittest.TestCase):
    def setUp(self) -> None:
        self.dag = DAG(DB)

    def tearDown(self) -> None:
        pass

    def test_loadDB(self):
        res = self.dag.load_dag()

        self.assertTrue(res)

    def test_addtx(self):
        tx_key, _ = self.dag.add_tx(TX(from_="LJS", to_="YTH", data={"value": 5000}))
        tx_key2, _ = self.dag.add_tx(TX(from_="LJS", to_="YTH", data={"value": 10000}, status=2))

        tx_val = json.loads(DB.get(tx_key.encode()).decode())
        tx_val2 = json.loads(DB.get(tx_key2.encode()).decode())

        self.assertEqual(self.dag.txs[tx_key], tx_val)
        self.assertEqual(self.dag.txs[tx_key2], tx_val2)



if __name__ == '__main__':
    unittest.main()   # python -m unittest -v test/db_test.py
