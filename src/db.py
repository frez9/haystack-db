from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask

from flask_script import Manager 
from flask_migrate import Migrate, MigrateCommand

db = SQLAlchemy()

app = Flask(__name__)
db_filename = "haystack.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
db.init_app(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String, nullable=False)
    display_name = db.Column(db.String, nullable=True)
    avatar_url = db.Column(db.String, nullable=True)
    notification_token = db.Column(db.String, nullable=True)
    phone_number = db.Column(db.String, nullable=True)
    time_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        self.external_id = kwargs.get('external_id')
        self.display_name = kwargs.get('display_name')
        self.avatar_url = kwargs.get('avatar_url')
        self.notification_token = kwargs.get('notification_token')
        self.phone_number = kwargs.get('phone_number')

    def serialize(self):
        return {
            'id': self.id,
            'external_id': self.external_id,
            'avatar_url': self.avatar_url,
            'notification_token': self.notification_token,
            'phone_number': self.phone_number
        }

class Listing(db.Model):
    __tablename__ = 'listing'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_image_url = db.Column(db.String, nullable=False)
    avatar_url = db.Column(db.String, nullable=True)
    price = db.Column(db.Float, nullable=False)
    views = db.Column(db.Integer, nullable=False)
    sold = db.Column(db.Boolean, nullable=False)
    description = db.Column(db.String, nullable=True)
    condition = db.Column(db.Integer, nullable=False)
    time_created = db.Column(db.DateTime, default=datetime.utcnow)
    reports = db.relationship('Report', cascade='delete')
    favorites = db.relationship('Favorite', cascade='delete')

    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.product_image_url = kwargs.get('product_image_url')
        self.avatar_url = kwargs.get('avatar_url')
        self.price = kwargs.get('price')
        self.description = kwargs.get('description')
        self.condition = kwargs.get('condition')
        self.views = 0 
        self.sold = False 

    def serialize(self):
        favorites = [x.serialize() for x in self.favorites]
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_image_url': self.product_image_url,
            'avatar_url': self.avatar_url,
            'price': self.price,
            'views': self.views,
            'sold': self.sold,
            'description': self.description,
            'condition': self.condition,
            'reports': [x.serialize() for x in self.reports],
            'favorites': favorites,
            'favorite_count': len(favorites)
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

class Block(db.Model):
    __tablename__ = 'block'
    id = db.Column(db.Integer, primary_key=True)
    blocker_id = db.Column(db.Integer, nullable=False)
    blockee_id = db.Column(db.Integer, nullable=False)
    time_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        self.blocker_id = kwargs.get('blocker_id')
        self.blockee_id = kwargs.get('blockee_id')

    def serialize(self):
        return {
            'id': self.id,
            'blocker_id': self.blocker_id,
            'blockee_id': self.blockee_id
        }

if __name__ == '__main__':
    manager.run()