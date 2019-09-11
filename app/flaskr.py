
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
from app import app, db, rrclient, alt_rrclient
from app.models import User, Log, Key

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
        if user:
            if user.check_password(password):
                login_user(user, remember=True)
                flash('Successfully loggend in.', 'success')
                if request.args.get("next"):
                    return redirect(request.args.get('next'))
                return redirect(url_for('index'))
            flash('Password Incorrect.', 'warning')
            return render_template('site/login.html', login_email=email)
        flash('Email not found.', 'warning')
    return render_template('site/login.html')


@app.route("/register", methods=["POST"])
def register():
    """Register a new user"""
    name = request.form['name'] if 'name' in request.form else None
    email = request.form['email'] if 'email' in request.form else None
    password = request.form['password'] if 'email' in request.form else None

    if name is None:
        flash('Fill in the name.', 'warning')
        return render_template('login.j2')

    if email is None:
        flash('Fill in the email.', 'warning')
        return render_template(
            'login.j2',
            name=name
        )

    if password is None:
        flash('Fill in the password.', 'warning')
        return render_template(
            'login.j2',
            name=name,
            email=email
        )

    user = User.query.filter(User.email == email).first()
    if user is not None:
        flash('Email already taken.', 'warning')
        return render_template(
            'login.j2',
            name=name,
        )

    user = User()
    user.name = name
    user.email = email
    user.password = password
    db.session.add(user)
    db.session.commit()
    login_user(user)

    flash('Successfully registered account "%s".' % (user.name), 'success')
    if request.args.get("next") is not None:
        return redirect(request.args.get("next"))
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
    return [{'text': user.email, 'url': user.name}]


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
    key.key = ''.join(random.sample(
        string.ascii_letters + string.digits, 32
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


@app.route('/api/request/<path:url_path>', methods=["GET"])
def api_get(url_path):
    """Check key"""
    if 'Authorization' not in request.headers:
        return abort(403)

    authorization = request.headers['authorization']
    key = Key.query.filter(Key.key == authorization).first()
    if not key or not key.active:
        return abort(403)

    log = Log()
    log.date_time = datetime.now()
    log.key_id = key.id
    log.request_type = 'GET'
    log.request_url = url_path
    db.session.add(log)
    db.session.commit()

    alt = request.args.get('alt')
    if alt:
        result = alt_rrclient.get(url_path)
    else:
        result = rrclient.get(url_path)

    log.succes = True
    db.session.commit()
    return result


@app.route('/api/request/<path:url_path>', methods=["POST"])
def api_post(url_path):
    """Check key"""
    if 'Authorization' not in request.headers:
        return abort(403)

    authorization = request.headers['authorization']
    key = Key.query.filter(Key.key == authorization).first()
    if not key or not key.active:
        return abort(403)

    log = Log()
    log.date_time = datetime.now()
    log.key_id = key.id
    log.request_type = 'POST'
    log.request_url = url_path
    db.session.add(log)
    db.session.commit()

    if request.json:
        data = request.json
    else:
        data = {}

    alt = request.args.get('alt')
    if alt:
        result = alt_rrclient.post(url_path, data=data)
    else:
        result = rrclient.post(url_path, data=data)

    log.succes = True
    db.session.commit()
    return result


@app.route('/api/send_chat/<string:language>', methods=["POST"])
def api_send_chat(language):
    """Check key"""
    if 'Authorization' not in request.headers:
        return abort(403)

    authorization = request.headers['authorization']
    key = Key.query.filter(Key.key == authorization).first()
    if not key or not key.active:
        return abort(403)

    if 'message' not in request.json:
        return abort(400)

    message = request.json['message']

    log = Log()
    log.date_time = datetime.now()
    log.key_id = key.id
    log.request_type = 'CHAT'
    log.request_url = language
    db.session.add(log)
    db.session.commit()

    alt = request.args.get('alt')
    if alt:
        alt_rrclient.send_chat(language, message)
    else:
        rrclient.send_chat(language, message)

    log.succes = True
    db.session.commit()
    return json.dumps(True)
