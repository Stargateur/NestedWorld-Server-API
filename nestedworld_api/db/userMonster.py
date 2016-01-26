import arrow
import sqlalchemy_utils as sau
from . import db


class UserMonster(db.Model):

    __tablename__ = 'userMonsters'

    id = db.Column(db.Integer, primary_key=True, doc='UserMonster ID')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    monster_id = db.Column(db.Integer, db.ForeignKey('monsters.id'))
    monster = db.relationship('Monster')
    user = db.relationship('User')
    surname = db.Column(db.String, doc="Monster surname")
    experience = db.Column(db.Integer, doc="Monster experience")
    level = db.Column(db.Integer, doc="Monster level")