from marshmallow import Schema, fields
from kudag.dag import TX


class TxSchema(Schema):
    ver = fields.Int()
    timestamp = fields.Float()
    nonce = fields.Int()
    height = fields.Int()
    from_ = fields.Str()
    to_ = fields.Str()
    sign = fields.Str()
    data = fields.Dict(keys=fields.Str(), values=fields.Field())
    prts = fields.List(fields.Field())
    clds = fields.List(fields.Field())
    id = fields.Str()

    # meta data
    trusty = fields.Int()
    good = fields.Int()
    bad = fields.Int()
    status = fields.Int()
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