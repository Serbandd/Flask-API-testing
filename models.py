from extentions import db
from datetime import datetime

class User(db.Model):
    userID = db.Column(db.Integer, primary_key=True)
    cardNumber = db.Column(db.String, unique=True, nullable=False)
    PIN = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    accounts = db.relationship('Account', backref='user', lazy=True, cascade='all, delete-orphan')

    # ... other fields

class Account(db.Model):
    accountID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    transactions = db.relationship('Transaction', backref='account', lazy=True, cascade='all, delete-orphan')


class Transaction(db.Model):
    transactionID = db.Column(db.Integer, primary_key=True)
    accountID = db.Column(db.Integer, db.ForeignKey('account.accountID'), nullable=False)
    type = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)