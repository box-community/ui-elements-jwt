# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from email.policy import default
import hashlib
from flask_login import UserMixin

from apps import db, login_manager

from apps.authentication.util import hash_pass

class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    avatar_url = db.Column(db.String(512))
    access_token = db.Column(db.String(512))
    refresh_token = db.Column(db.String(512))
    box_user_id = db.Column(db.String(64),unique=True)
    box_demo_folder_id = db.Column(db.String(64),unique=False)
    csrf_token = db.Column(db.String(100), unique=True)

    def __init__(self, **kwargs):
        email = kwargs.get('email')
        avatar_url = kwargs.get('avatar_url')
        if avatar_url is None:
            avatar_url = 'https://www.gravatar.com/avatar/' + hashlib.md5(email.lower().encode('utf-8')).hexdigest() + '?d=identicon'
            setattr(self, 'avatar_url', avatar_url)
        
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('email')
    user = Users.query.filter_by(username=username).first()
    return user if user else None

# @login_manager.request_loader
# def request_loader(request):
#     username = request.form.get('username')
#     user = Users.query.filter_by(username=username).first()
#     return user if user else None