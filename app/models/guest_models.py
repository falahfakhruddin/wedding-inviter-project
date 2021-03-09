from app import db


class GuestList(db.Document):
    invitation_code = db.StringField()
    name = db.StringField()
    surname = db.StringField()
    group = db.StringField()
    phone = db.LongField()
    created_at = db.DateTimeField()

    meta = {
        'collections': 'guest_list',
        'indexes': [
            'name',
            'group'
        ]
    }


class GuestStatus(db.Document):
    name = db.StringField()
    attending = db.BooleanField()
    comment = db.StringField()

    meta = {
        'collections': 'guest_status',
        'indexes': [
            'name'
        ]
    }
