from mongoengine import *

connect('mqtt', host="mongo", port=27017)

class User(Document):
    email = StringField(require=True, unique=True)
    rfid = ListField(IntField(),require=True, unique=True)
    name = StringField(max_length=50)
    last_time = DateTimeField()
    last_address = StringField()
    last_number = IntField()
    usage_times = IntField(default=0)
    is_used = BooleanField(default=False)

class IOT(Document):
    number = IntField(require=True, unique=True)
    address = StringField(require=True)
    usage_times = IntField(default=0)
    is_used = BooleanField(default=False)
    last_time = DateTimeField()
    last_user = StringField()
    rfid = ListField(IntField())
    is_online = BooleanField(default=False)
    online_time = DateTimeField()
