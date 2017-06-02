from flask import render_template, session, redirect, url_for, current_app, flash
from datetime import datetime
from .. import mongo
from ..models import User, Miner
from . import main
from .forms import LoginForm, RegistrationForm
from .table import BlockchainTable


@main.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User(username=username, password=password)

        # Attempt to login
        response, success = user.login_user()
        flash(response)
        return render_template('index.html',
                               form=form, name=session.get('name'),
                               known=session.get('known', False))

    return render_template('index.html',
                           form=form, name=session.get('name'),
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

        # If registration was successful, initialise the user and give them some coins
        if registration_success:
            miner = Miner()
            miner.initialise_new_user(user)

        flash(response)

    return render_template('register.html',
                           form=form)


@main.route('/blockchain-log', methods=['GET', 'POST'])
def blockchain_log():
    # Insert some test table entries
    blockchain_transactions = mongo.db.blockchain.find()
    table_list = []

    for transaction in blockchain_transactions:
        table_list.append({
            'from_user': 'Alice',
            'to_user': 'Bob',
            'amount': transaction['cc_amount'],
            'timestamp': transaction['timestamp'],
            'nonce': transaction['nonce'],
            'miner_verify': transaction['miner_verify']
        })

    table = BlockchainTable(table_list)

    return render_template('blockchain-log.html',
                           table=table)

# def index():
#
#     form = NameForm()
#
#     # if form.validate_on_submit():
#     #     user = User.query.filter_by(username=form.name.data).first()
#     #     if user is None:
#     #         user = User(username=form.name.data)
#     #         db.session.add(user)
#     #         session['known'] = False
#     #     else:
#     #         session['known'] = True
#     #     session['name'] = form.name.data
#     #     return redirect(url_for('.index'))
#     return render_template('index.html',
#                            form=form, name=session.get('name'),
#                            known=session.get('known', False))
