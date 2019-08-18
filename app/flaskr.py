
"""
Simple flask thing
"""

import random
import string
from datetime import datetime
from flask import render_template, request, redirect, \
    flash, url_for, abort, json
from flask_breadcrumbs import Breadcrumbs, register_breadcrumb
from flask_menu import Menu, register_menu
from flask_login import login_required, login_user, logout_user
from app import app, login_manager, db
from app.models import User, Request, Log, Key

Menu(app=app)
Breadcrumbs(app=app)


@register_breadcrumb(app, '.login', 'Login')
@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle login page and data"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter(User.email == email).first()
        if user is not None:
            if user.password == password:
                login_user(user)
                flash('You were successfully logged in', 'success')
                if request.args.get("next") is not None:
                    return redirect(request.args.get("next"))
                else:
                    return redirect(url_for('index'))
            else:
                flash('Incorrect password', 'danger')
        else:
            flash('User not found', 'danger')

        return redirect(url_for('login'))
    else:
        return render_template('site/login.html')


@app.route("/register", methods=["POST"])
def register():
    """Register a new user"""
    user = User()
    user.name = request.form['name']
    user.email = request.form['email']
    user.password = request.form['password']
    db.session.add(user)
    db.session.commit()
    login_user(user)
    flash('Succesfully registered account', 'success')
    if request.args.get("next") is not None:
        return redirect(request.args.get("next"))
    else:
        return redirect(url_for('index'))


@app.route("/logout")
@login_required
def logout():
    """Logout function for users"""
    logout_user()
    flash('succesfully logged out', 'success')
    return redirect(url_for('login'))


@app.route('/')
@register_menu(app, '.', 'Home')
@register_breadcrumb(app, '.', 'Home')
def index():
    """Show homepage"""
    # users = User.query.count()
    return render_template('site/index.html')
    # return render_template('site/index.html', users=users)


@app.route('/users')
@register_menu(app, 'users', 'Users')
@register_breadcrumb(app, '.users', 'Users')
@login_required
def user_index():
    """Show users"""
    users = User.query.all()
    return render_template('user/index.html', users=users)


def user_overview_dlc(*args, **kwargs):
    """Generate dynamic_list for user"""
    id = request.view_args['id']
    user = User.query.get(id)
    return [{'text': user.email, 'url': user.url}]


@app.route('/user/<int:id>')
@register_breadcrumb(app, '.users.id', '',
                     dynamic_list_constructor=user_overview_dlc)
@login_required
def user_overview(id):
    """Show user overview"""
    id = int(id)
    user = User.query.get(id)
    return render_template('user/overview.html', user=user)


@app.route('/user/<int:id>/generate_key')
@login_required
def user_generate_key(id):
    """Generate new key for user"""
    user = User.query.get(id)
    key = Key()
    key.key = ''.join(random.choices(
        string.ascii_letters + string.digits, k=64
    ))
    key.user_id = user.id
    db.session.add(key)
    db.session.commit()
    flash('Succesfully generated key', 'success')
    return redirect(url_for('user_overview', id=user.id))


@app.route('/user/<int:user_id>/key/<int:key_id>/activate')
@login_required
def user_toogle_key(user_id, key_id):
    """Activate key"""
    user = User.query.get(user_id)
    key = Key.query.get(key_id)
    key.active = not key.active
    db.session.add(key)
    db.session.commit()

    if key.active:
        flash('Activated key', 'success')
    else:
        flash('Deactivated key', 'success')

    return redirect(url_for('user_overview', id=user.id))


@app.route('/api/authenticated', methods=["POST"])
def api_authenticated():
    """Check key"""
    if 'Authorization' not in request.headers:
        return abort(403)

    authorization = request.headers['authorization']
    key = Key.query.filter(Key.key == authorization).count()

    if key:
        return json.dumps(True)

    return json.dumps(False)


@app.route('/api/request', methods=["GET"])
def api_log():
    """Check key"""
    if 'Authorization' not in request.headers:
        return abort(403)

    authorization = request.headers['authorization']
    key = Key.query.filter(Key.key == authorization).first()
    if not key or not key.active:
        return abort(403)

    log = Log()

    db.session.add(log)
    db.session.commit()

    return json.dumps(True)