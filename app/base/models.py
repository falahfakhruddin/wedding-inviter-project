# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin

from app import db, login_manager

from app.base.util import hash_pass


class User(db.Document, UserMixin):

    username = db.StringField(unique=True)
    email = db.StringField(unique=True)
    password = db.BinaryField(unique=True)

    def clean(self):
        self.password = hash_pass(self.password)

    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    return User.objects(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.objects(username=username).first()
    return user if user else None
