from marshmallow import Schema, fields
from datetime import datetime

USERS = {"user1":{'id':0, 'username':"PMS", 'lang':['python', 'java'], 'created_at': '2011-11-04T00:00:00'}}

class User:
    def __init__(self, id, username, password, lang):
        self.id = id
        self.username = username
        self.password = password
        self.lang = lang
        self.created_at = datetime.now()

class UserSchema(Schema):
    # read-only, It generate Validation Error  when schema load
    # POST할 때 dump_only인 key의 value 입력하면 parse error.
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    # write-only, schema dump할 때 load_only인 값은 안넘어감
    password = fields.Str(load_only=True, data_key="my-password")
    lang = fields.List(fields.Str())
    created_at = fields.DateTime()

user1 = User(2, "LJS", "myrandompasswd", lang=["python", "java"])
res = UserSchema().dump(user1)  # serialize obj to native python data types
print(res)
temp_id = int(max(USERS.keys()).lstrip('user')) + 1
USERS[f'user{temp_id}'] = res

for k in USERS.keys():
    del USERS[k]['id']

print(UserSchema().load(USERS['user1']))  # deserialize a data structure to an object by schema field
print(UserSchema().load(USERS['user2']))
