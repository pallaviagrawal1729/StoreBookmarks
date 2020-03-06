from datetime import datetime
from bookmarkProject import db
from sqlalchemy import desc
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    @staticmethod
    def new_bookmarks(num):
        return Bookmark.query.order_by(desc(Bookmark.date)).limit(num)

    def __repr__(self):
        return "<Bookmark '{}' : '{}'>".format(self.description, self.url)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    bookmarks = db.relationship('Bookmark', backref='user', lazy='dynamic')
    # This will not containt password itself, but a secured hash
    password_hash = db.Column(db.String)

    # Note the password_hash will not be represented in a database table, and if we try to read it directly it raises
    # an AttributeError we use python property to make this field a write only so that we can write a value as string
    # but read it as hash only.
    @property
    def password(self):
        raise AttributeError('password: write-only field')

    # The setter generates a hash for password and store it in its hash value
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    #it will take password as string, hash it and compare the hash values
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    def __repr__(self):
        return '<User %r>' % self.username
