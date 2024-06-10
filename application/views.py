from flask import config, render_template, redirect, url_for, Blueprint, current_app, request, flash, send_from_directory
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from .models import User
from .forms import LoginForm
from application import login
from werkzeug.urls import url_parse

bp_name = 'bp'
bp = Blueprint(bp_name, __name__)

@bp.route('/')
def index():
    if current_user.is_anonymous:
        return redirect(url_for('bp.login'))
    return render_template('index.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('bp.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('bp.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('bp.index')
        return redirect(next_page)
        
    return render_template('login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('bp.index'))

@bp.route('/hidden')
@login_required
def hidden():
    return "You shouldn't  see this when you are not logged in!"

@bp.route('/visible')
def visible():
    return "This content is visible for all!"
