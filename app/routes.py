from flask import render_template, redirect, url_for, flash, Blueprint
from app.forms import LoginForm
from app.utils import check_user_credentials
import os





main = Blueprint('main', __name__)



@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if check_user_credentials(username=username, password=password):
            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))    
        else:
            flash('Login failed. Check your username and password.', 'danger')           
    return render_template('login.html', form=form)

@main.route('/dashboard')
def dashboard():
    return "<h1>Welcome to the Dashboard!</h1>"


@main.route('/')
def index():
    return redirect(url_for('main.login'))          


