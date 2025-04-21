from flask import Blueprint, render_template, redirect, url_for
from models import Habit, db
from datetime import date
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    return render_template('index.html')

@main_bp.route('/home')
@login_required
def home():
    """Dashboard showing all habits with streaks"""
    habits = Habit.query.filter_by(user_id=current_user.id).all()
    today = date.today()
    return render_template('home.html', habits=habits, today=today)

@main_bp.route('/about')
def about():
    return render_template('about.html')