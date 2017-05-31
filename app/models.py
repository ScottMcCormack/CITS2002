from . import db
import hashlib


class User(db.Document):
    username = db.StringField(required=True)
    password_hash = db.StringField(required=True)

    def __repr__(self):
        return '<User %r>' % self.username
