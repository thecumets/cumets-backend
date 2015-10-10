from datetime import datetime

from database import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)
    name = db.Column(db.String, nullable=False)
    token_id = db.Column(db.String, nullable=False, index=True)
    facebook_id = db.Column(db.String, nullable=False, index=True)
    last_latitude = db.Column(db.Integer, nullable=True)
    last_longitude = db.Column(db.Integer, nullable=True)

    activities = db.relationship('Activity', backref='user', lazy='dynamic', foreign_keys="Activity.user_id")


class Activity(db.Model):
    __tablename__ = 'activity'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    disrupted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    ended_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    disrupted_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)


class House(db.Model):
    __tablename__ = 'house'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Integer, nullable=False)
    longitude = db.Column(db.Integer, nullable=False)
