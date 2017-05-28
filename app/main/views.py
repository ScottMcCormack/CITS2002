from flask import render_template, session, redirect, url_for, current_app
from requests import request
# from .. import db
from .. import redis_db
# from ..models import User
from . import main
from .forms import NameForm, RegistrationForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = RegistrationForm()

    if request.method == 'POST' and form.validate_on_submit():
        pass
    #     user = User(form.username.data, form.email.data,
    #                 form.password.data)
    #     db_session.add(user)
    #     flash('Thanks for registering')
    #     return redirect(url_for('login'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False))

# def index():
#     # count = redis_db.incr('hits')
#     # return 'Hello from Docker! I have been seen {} times!!!!\n'.format(count)
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
