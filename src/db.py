from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String, nullable=False)
    avatar_url = db.Column(db.String, nullable=True)
    snapchat_username = db.Column(db.String, nullable=True)
    time_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        self.external_id = kwargs.get('external_id')
        self.avatar_url = kwargs.get('avatar_url')

    def serialize(self):
        return {
            'id': self.id,
            'external_id': self.external_id,
            'avatar_url': self.avatar_url,
            'snapchat_username': self.snapchat_username
        }

class Listing(db.Model):
    __tablename__ = 'listing'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_image_url = db.Column(db.String, nullable=False)
    avatar_url = db.Column(db.String, nullable=True)
    time_created = db.Column(db.DateTime, default=datetime.utcnow)
    reports = db.relationship('Report', cascade='delete')
    favorites = db.relationship('Favorite', cascade='delete')

    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.product_image_url = kwargs.get('product_image_url')
        self.avatar_url = kwargs.get('avatar_url')

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_image_url': self.product_image_url,
            'avatar_url': self.avatar_url,
            'reports': [x.serialize() for x in self.reports],
            'favorites': [x.serialize() for x in self.favorites]
        }

class Report(db.Model):
    __tablename__ = 'report'
    id = db.Column(db.Integer, primary_key=True)
    report = db.Column(db.String, nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'), nullable=False)
    time_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        self.report = kwargs.get('report')
        self.listing_id = kwargs.get('listing_id')

    def serialize(self):
        return {
            'id': self.id,
            'report': self.report,
            'listing_id': self.listing_id
        }

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'), nullable=False)
    time_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.listing_id = kwargs.get('listing_id')

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'listing_id': self.listing_id
        }
