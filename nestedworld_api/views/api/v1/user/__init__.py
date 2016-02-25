from marshmallow import post_dump
from marshmallow.validate import OneOf
from nestedworld_api.app import ma
from nestedworld_api.login import login_required, current_session
from .. import api

user = api.namespace('users')

from . import auth
from . import monsters
from . import friends
from . import inventory

@user.route('/')
class User(user.Resource):
    tags = ['users']

    class Schema(ma.Schema):
        email = ma.Email()
        pseudo = ma.String()
        birth_date = ma.Date()
        city = ma.String()
        gender = ma.String(validate=[OneOf(['female', 'male', 'other'])])
        avatar = ma.Url()
        background = ma.Url()
        registered_at = ma.DateTime(dump_only=True)
        is_active = ma.Boolean(dump_only=True)

        @post_dump(pass_many=True)
        def add_envelope(self, data, many):
            namespace = 'users' if many else 'user'
            return {namespace: data}

    @login_required
    @user.marshal_with(Schema())
    def get(self):
        user = current_session.user

        return user

    @login_required
    @user.accept(Schema())
    @user.marshal_with(Schema())
    def put(self, data):
        from nestedworld_api.db import db
        from nestedworld_api.db import User

        user = current_session.user

        conflict = User.query\
                       .filter(User.id != user.id)\
                       .filter((User.email == user.email) | (User.pseudo == user.pseudo))\
                       .first()
        if conflict is not None:
            user.abort(400, 'An user with same email/pseudo already exists')

        for (name, value) in data.items():
            setattr(user, name, value)

        db.session.commit()

        return user

from . import auth
from . import monsters
from . import friends
