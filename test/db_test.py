import unittest
import json
import plyvel
from pathlib import Path

from kudag.dag import TX, DAG


class Database(unittest.TestCase):
    def setUp(self) -> None:
        db_path = Path(__file__).parents[0].joinpath("db/")
        if not db_path.exists():
            db_path.mkdir(parents=True)
        self.DB = plyvel.DB(str(db_path), create_if_missing=True)
        self.dag = DAG(self.DB)

    def tearDown(self) -> None:
        pass

    def test_loadDB(self):
        res = self.dag.load_dag()

        self.assertTrue(res)

    def test_addtx(self):
        tx_key, _ = self.dag.add_tx(TX(from_="LJS", to_="YTH", data={"value": 5000}))
        tx_key2, _ = self.dag.add_tx(TX(from_="LJS", to_="YTH", data={"value": 10000}, status=2))

        tx_val = json.loads(self.DB.get(tx_key.encode()).decode())
        tx_val2 = json.loads(self.DB.get(tx_key2.encode()).decode())

        self.assertEqual(self.dag.txs[tx_key], tx_val)
        self.assertEqual(self.dag.txs[tx_key2], tx_val2)



if __name__ == '__main__':
    unittest.main()   # python -m unittest -v test/db_test.py
