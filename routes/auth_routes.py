from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from models import User, db
from werkzeug.security import generate_password_hash
import re

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = 'remember' in request.form
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            flash('Invalid username or password', 'danger')
            return render_template('auth/login.html')
            
        login_user(user, remember=remember)
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('main.home')
            
        flash(f'Welcome back, {user.username}!', 'success')
        return redirect(next_page)
        
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Basic validation
        errors = []
        
        if User.query.filter_by(username=username).first():
            errors.append('Username already exists')
            
        if User.query.filter_by(email=email).first():
            errors.append('Email already registered')
            
        if password != confirm_password:
            errors.append('Passwords do not match')
            
        if len(password) < 8:
            errors.append('Password must be at least 8 characters long')
            
        if not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password):
            errors.append('Password must contain both letters and numbers')
            
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            errors.append('Invalid email format')
            
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('auth/register.html')
            
        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        # Auto-login the user after registration
        login_user(new_user)
        
        flash(f'Welcome to Habit Tracker, {new_user.username}!', 'success')
        return redirect(url_for('main.home'))
        
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html')
