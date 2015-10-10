from datetime import datetime

from database import db


user_to_relationship = db.Table(
    'relationships',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('relationship_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

class Subsciption(db.Model):
    __tablename__ = 'subsciption'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    email = db.Column(db.String,nullable=False)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)
    name = db.Column(db.String, nullable=False)
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


class Activity(db.Model):
    __tablename__ = 'activity'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    disrupted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    ended_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    disrupted_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    def __init__(self, user_id):
        self.user_id = user_id
