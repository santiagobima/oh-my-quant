from flask import render_template, redirect, url_for, flash, Blueprint, session
from app.forms import LoginForm
from app.utils import check_user_credentials, get_user_role, login_required, role_required
import os


main = Blueprint('main', __name__)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if check_user_credentials(username=username, password=password):
            role = get_user_role(username) or 'client'
            session['username'] = username
            session['role'] = role
            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))    
        else:
            flash('Login failed. Check your username and password.', 'danger')           
    return render_template('login.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    username = session.get('username')
    role = session.get('role','client') 
    template = 'dashboard_admin.html' if role == 'admin' else 'dashboard_client.html'
    return render_template(template, username=username, role=role) 

@main.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))



@main.route('/')
def index():
    return redirect(url_for('main.login'))          


@main.route('/admin-only')
@login_required
@role_required('admin')
def admin_only_page():
    return "<h1>Welcome Admin! This is a restricted page.</h1>"