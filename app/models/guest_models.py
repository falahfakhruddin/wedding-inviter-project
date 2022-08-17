from app import db


class GuestList(db.Document):
    name = db.StringField()
    group = db.StringField()
    created_at = db.DateTimeField()
    shared_at = db.DateTimeField()

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


class TemplateMessage(db.Document):
    name = db.StringField(unique=True)
    template = db.StringField()

    meta = {
        'collections': 'template_message'
    }