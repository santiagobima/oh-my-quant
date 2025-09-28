from flask import render_template, redirect, url_for, flash, Blueprint,jsonify, session
from app.forms import LoginForm
from app.utils import check_user_credentials, get_user_role, login_required, role_required
import os
import subprocess
from datetime import datetime
import psycopg2
import pandas as pd 




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
    
    last_update = None
    try:
        with psycopg2.connect(os.getenv('DATABASE_URL')) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT MAX(trade_date) FROM prices_eod;')
                result = cur.fetchone()
                if result and result[0]:
     
                    last_update = result[0].strftime('%Y-%m-%d')
    except Exception as e:
        print(f"Error fetching last update date: {e}")
        last_update = 'Unknown'
    
    return render_template(template, username=username, role=role, last_update=last_update) 




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



@main.route('/fetch-latest', methods=['POST'])
@login_required
def fetch_latest():
    try:
        # Lanza el script en segundo plano (no bloquea)
        subprocess.Popen(
            ['python3', 'scripts/seed_market.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        flash('Market data fetching started...', 'info')
    except Exception as e:
        flash(f'Exception occurred: {str(e)}', 'danger')

    # Redirige al spinner inmediatamente
    return redirect(url_for('main.fetching'))


@main.route('/fetching')
@login_required
def fetching():
    return render_template("fetching.html")


        
    
 
        
