from datetime import datetime
from geoalchemy2.types import Geography

from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)
    name = db.Column(db.String, nullable=False)
    profile_url = db.Column(db.String, nullable=False)
    access_token = db.Column(db.String, nullable=False)
    last_position = db.Column(Geography(geometry_type='POINT', srid=4326), nullable=True)

    activities = db.relationship('Activity', backref='user', lazy='dynamic')


class Activity(db.Model):
    __tablename__ = 'activity'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    disrupted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    ended_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    disrupted_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    disrupter = db.relationship("User", foreign_keys="Activity.disrupted_by")


class House(db.Model):
    __tablename__ = 'house'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String, nullable=False)
    position = db.Column(Geography(geometry_type='POINT', srid=4326), nullable=False)
