from datetime import datetime
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context as pwd_context

from database import db
from app import app

user_to_relationship = db.Table(
    'relationships',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('relationship_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)


class Subscription(db.Model):
    __tablename__ = 'subscription'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    email = db.Column(db.String, nullable=False)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)
    name = db.Column(db.String, nullable=False)
    token = db.Column(db.String, nullable=True)
    token_id = db.Column(db.String, nullable=False, index=True)
    facebook_id = db.Column(db.String, nullable=False, index=True)
    last_latitude = db.Column(db.Float, nullable=True)
    last_longitude = db.Column(db.Float, nullable=True)
    gcm = db.Column(db.String, nullable=True)

    activities = db.relationship('Activity', backref='user', lazy='dynamic', foreign_keys="Activity.user_id")
    relationships = db.relationship("User", secondary=user_to_relationship,
                                    primaryjoin=id == user_to_relationship.c.user_id,
                                    secondaryjoin=id == user_to_relationship.c.relationship_id,
                                    backref="other_relationships"
                                    )

    def hash_password(self, facebook_id):
        self.token = pwd_context.encrypt(facebook_id)

    def verify_password(self, facebook_id):
        return pwd_context.verify(facebook_id, self.token)

    def generate_auth_token(self, expiration=3600 * 24 * 365):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user


class Activity(db.Model):
    __tablename__ = 'activity'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    disrupted_at = db.Column(db.DateTime, default=None, nullable=True)
    ended_at = db.Column(db.DateTime, default=None, nullable=True)
    disrupted_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    def __init__(self, user_id):
        self.user_id = user_id

    def disrupt(self, disrupter):
        self.disrupted_by = disrupter
        self.disrupted_at = datetime.utcnow()
        self.ended_at = datetime.utcnow()
