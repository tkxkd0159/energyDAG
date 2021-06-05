from marshmallow import Schema, fields
from lib.dag import TX


class TxSchema(Schema):
    ver = fields.Int()
    timestamp = fields.Float()
    prts = fields.List(fields.Field())
    clds = fields.List(fields.Field())
    height = fields.Int()
    id = fields.Str()
    sign = fields.Str()
    data = fields.List(fields.Str())
    trusty = fields.Int()
    good = fields.Int()
    bad = fields.Int()
    status = fields.Int()
    nonce = fields.Int()
    conflTX = fields.List(fields.Field())
    tArriv = fields.Int()
    tConfl = fields.Int()
    tConf = fields.Int()
    tStale = fields.Int()
    validators = fields.List(fields.Field())

if __name__ == "__main__":

    mytx = TX()
    mytx_dict = mytx.serialize()
    res = TxSchema().load(mytx_dict)
    res2 = TxSchema().dump(mytx)

    print(res)
    print(res2)