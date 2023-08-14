from flask import Blueprint, jsonify, request
from extentions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from models import Account, Transaction


transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/withdraw', methods=['POST'])
#@jwt_required()  # Require a valid token
def withdraw():
    user_id = get_jwt_identity()

    try:
        account_id = request.json['accountID']
        amount = float(request.json['amount'])
    except KeyError:
        return jsonify({"msg": "Missing required parameters"}), 400

    account = Account.query.filter_by(accountID=account_id, userID=user_id).first()
    if account is None:
        return jsonify({"msg": "Account not found"}), 404
    if account.balance < amount:
        return jsonify({"msg": "Insufficient funds"}), 400

    account.balance -= amount
    transaction = Transaction(accountID=account_id, type="withdrawal", amount=amount, timestamp=datetime.utcnow())
    db.session.add(transaction)
    db.session.commit()

    return jsonify({"msg": "Withdrawal successful", "balance": account.balance}), 200

@transactions_bp.route('/deposit', methods=['POST'])
#@jwt_required()  # Require a valid token
def deposit():
    user_id = get_jwt_identity()

    try:
        account_id = request.json['accountID']
        amount = float(request.json['amount'])
    except KeyError:
        return jsonify({"msg": "Missing required parameters"}), 400

    account = Account.query.filter_by(accountID=account_id, userID=user_id).first()
    if account is None:
        return jsonify({"msg": "Account not found"}), 404

    account.balance += amount
    transaction = Transaction(accountID=account_id, type="deposit", amount=amount, timestamp=datetime.utcnow())
    db.session.add(transaction)
    db.session.commit()

    return jsonify({"msg": "Deposit successful", "balance": account.balance}), 200