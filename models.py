from datetime import datetime

from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)
    name = db.Column(db.String, nullable=False)
    profile_url = db.Column(db.String, nullable=False)
    access_token = db.Column(db.String, nullable=False)
    last_latitude = db.Column(db.Float, nullable=True)
    last_longitude = db.Column(db.Float, nullable=True)

    activities = db.relationship('Activity', backref='user', lazy='dynamic')


class Activity(db.Model):
    __tablename__ = 'activity'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    interrupted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    ended_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    disrupted_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    giver = db.relationship("User", foreign_keys="Activity.giver_id")
    receiver = db.relationship("User", foreign_keys="Activity.receiver_id")
