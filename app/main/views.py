from flask import render_template, session, redirect, url_for, current_app, flash
from .. import mongo
from ..models import User, Miner
from . import main
from .forms import LoginForm, RegistrationForm, TransactionForm
from .table import BlockchainTable


@main.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User(username=username, password=password)

        # Attempt to login
        login_success, response = user.login_user()
        flash(response)

        # If successfully logged in set session to true
        if login_success:
            session['known'] = True
            session['name'] = username

            return render_template('index.html',
                                   form=False,
                                   name=session.get('name'),
                                   known=session.get('known', False))

    return render_template('index.html',
                           form=form,
                           name=session.get('name'),
                           known=session.get('known', False))


@main.route('/register', methods=['GET', 'POST'])
def register():
    # Allows a new user to register
    form = RegistrationForm()

    # Validate the form
    if form.validate_on_submit():
        # Get data from forms and initialise a 'user' object
        username = form.username.data
        password = form.password.data
        user = User(username=username, password=password)

        # Attempt to register a new user
        registration_success, response = user.register_new_user()
        flash(response)

        # If registration was successful, initialise the user and give them some coins
        if registration_success:
            miner = Miner()
            miner.initialise_new_user(user)

            # Log out any users and send them to the homepage to log in
            return redirect(url_for('.logout'))

    return render_template('register.html',
                           form=form,
                           known=session.get('known', False))


@main.route('/logout', methods=['GET'])
def logout():
    session['known'] = False
    session['name'] = False
    return redirect(url_for('.index'))


@main.route('/blockchain-log', methods=['GET'])
def blockchain_log():
    # Get all the blockchain transactions from the database 'blockchain'
    blockchain_transactions = mongo.db.blockchain.find()
    # Parse transactions and load them into 'table_list'
    table_list = []

    for transaction in blockchain_transactions:
        to_user_pk = transaction['to_user_pk']
        from_user_pk = transaction['from_user_pk']

        # Helper function to encode as 'UTF-8' if not:
        if isinstance(to_user_pk, str):
            to_user_pk = to_user_pk.encode('UTF-8')
        if isinstance(from_user_pk, str):
            from_user_pk = from_user_pk.encode('UTF-8')

        # Cross-reference user database to get actual username
        to_user = mongo.db.users.find_one(
            {'public_key': to_user_pk}
        )
        to_user_username = to_user['username']

        # If from 'miner' set from username as simply 'miner'
        if from_user_pk == b'<miner>':
            from_user_username = '<miner>'
        else:
            from_user = mongo.db.users.find_one(
                {'public_key': from_user_pk}
            )
            from_user_username = from_user['username']

        if to_user is not None:
            table_list.append({
                'from_user': from_user_username,
                'to_user': to_user_username,
                'amount': transaction['cc_amount'],
                'timestamp': transaction['timestamp'],
                'nonce': transaction['nonce'],
                'miner_verify': transaction['miner_verify']
            })

    table = BlockchainTable(table_list)

    return render_template('blockchain-log.html',
                           table=table,
                           known=session.get('known', False))


@main.route('/transactions', methods=['GET', 'POST'])
def transactions():
    # Determine if a user is currently logged in
    user_known = session.get('known', False)
    user_name = session.get('name', False)

    # If not redirect them back to the homepage
    if not user_known:
        flash('Please log in')
        return redirect(url_for('.index'))

    # Initialise the Transaction Form
    form = TransactionForm()

    # Get a list of users who we can send chriscoins to, excluding self
    username_list = User.get_username_list(username=user_name)
    form.to_user.choices = username_list

    if form.validate_on_submit():
        from_username = session['name']
        to_username = form.to_user.data
        amount = form.amount.data

        response = User.create_new_transaction(
            from_username=from_username,
            to_username=to_username,
            amount=amount
        )

        flash(response)

    return render_template('transactions.html', form=form,
                           known=user_known)
