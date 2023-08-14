from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from config import configure_app
from transactions_end_points import transactions_bp
from auth import auth_bp
from extentions import db, jwt
from models import User, Account, Transaction
from flask import Flask, render_template, request, redirect, url_for, flash


app = Flask(__name__)

# Register blueprints or import routes
app.register_blueprint(transactions_bp, url_prefix='/transactions')
app.register_blueprint(auth_bp)
configure_app(app)  # Apply configurations

db.init_app(app) # this first makes the connection.
def init_db():
    with app.app_context():
        try:
            print("creating tables")
            db.create_all()
        except Exception as e:
            print("An error occurred while creating tables:", e)
print("alalal")
init_db()

# Configuration (imported from config.py)
# ...
# Initialize extensions
# Initialize extensions

jwt.init_app(app)

@app.route('/')
def index():
    # Query the user and transactions
    user = User.query.first()  # Or use an appropriate filter to get the user
    # Fetching account linked to the user
    account = Account.query.filter_by(userID=user.userID).first()
    transactions = Transaction.query.filter_by(accountID=account.accountID).all()

    starting_balance = account.balance
    for tx in transactions:
        if tx.type == 'deposit':
            starting_balance -= tx.amount
        elif tx.type == 'withdraw':
            starting_balance += tx.amount

    balances = [starting_balance]
    balance = starting_balance
    for tx in transactions:
        if tx.type == 'deposit':
            balance += tx.amount
        elif tx.type == 'withdraw':
            balance -= tx.amount
        balances.append(balance)


    transactions_with_balances = zip(transactions, balances[1:])


    return render_template('index.html', user=user, starting_balance=balance, transactions_with_balances=transactions_with_balances, ending_balance = balance)

@app.route('/submit_transaction', methods=['POST'])
def submit_transaction():
    user = User.query.first()  # Again, fetching user based on the logged-in user
    account = Account.query.filter_by(userID=user.userID).first()

    deposit = float(request.form['deposit']) if request.form['deposit'] else 0
    withdraw = float(request.form['withdraw']) if request.form['withdraw'] else 0

    if deposit > 0:
        account.balance += deposit
        new_transaction = Transaction(accountID=account.accountID, type='deposit', amount=deposit)
        db.session.add(new_transaction)

    if withdraw > 0:
        if withdraw <= account.balance:
            account.balance -= withdraw
            new_transaction = Transaction(accountID=account.accountID, type='withdraw', amount=withdraw)
            db.session.add(new_transaction)
        else:
            flash('Cannot withdraw because of insufficient funds!', 'error')

    db.session.commit()

    return redirect(url_for('index'))

# Register blueprints or import routes
# ...
if __name__ == '__main__': 
    app.run(debug=True)