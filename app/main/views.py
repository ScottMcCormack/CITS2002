from flask import render_template, session, redirect, url_for, current_app, flash
from datetime import datetime
from .. import mongo
from ..models import User
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
        response = user.login_user()
        flash(response)


        # # Check to see if user already exists in the database
        # if user is None:
        #     flash('User doesn\'t exist!')
        # else:
        #     flash(user.password)

        return render_template('index.html',
                               form=form, name=session.get('name'),
                               known=session.get('known', False))

    # db_session.add(user)
    #     flash('Thanks for registering')
    #     return redirect(url_for('login'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False))


@main.route('/blockchain-log', methods=['GET', 'POST'])
def blockchain_log():
    # Insert some test table entries
    items = [
        dict(from_user='Alice', to_user='Bob', amount='50', timestamp=datetime.now(),
             nonce='1028', miner_verify=True),
        dict(from_user='Alice', to_user='Bob', amount='50', timestamp=datetime.now(),
             nonce='1028', miner_verify=True),
        dict(from_user='Alice', to_user='Bob', amount='50', timestamp=datetime.now(),
             nonce='1028', miner_verify=True),
    ]

    table = BlockchainTable(items)

    return render_template('blockchain-log.html',
                           table=table)


@main.route('/register', methods=['GET', 'POST'])
def register():
    # Allows a new user to register
    form = RegistrationForm()

    # Validate the form
    if form.validate_on_submit():
        # Determine to see if a user exists
        username = form.username.data
        password = form.password.data
        user = User(username=username, password=password)

        # Attempt to register a new user
        response = user.register_new_user()
        flash(response)

    return render_template('register.html',
                           form=form)

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
