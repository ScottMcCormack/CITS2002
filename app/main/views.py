from flask import render_template, session, redirect, url_for, current_app, flash
from .. import db
from ..models import User
from . import main
from .forms import LoginForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()

    if form.validate_on_submit():
        user = db.users.find_one({'username': form.username.data})

        # Check to see if user already exists in the database
        if user is None:
            flash('User doesn\'t exist!')
        else:
            flash('User exists in database')

    #     db_session.add(user)
    #     flash('Thanks for registering')
    #     return redirect(url_for('login'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False))

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
