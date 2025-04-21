from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, abort
from models import Habit, HabitLog, db
from datetime import date
from sqlalchemy import desc
from flask_login import login_required, current_user

habit_bp = Blueprint('habit', __name__)

@habit_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_habit():
    """Create a new habit"""
    if request.method == 'POST':
        name = request.form.get('name')
        color = request.form.get('color', '#3498db')
        icon = request.form.get('icon')
        
        if not name:
            flash('Habit name is required', 'error')
            return render_template('habit_form.html')
            
        habit = Habit(name=name, color=color, icon=icon, user_id=current_user.id)
        db.session.add(habit)
        db.session.commit()
        
        flash(f'Habit "{name}" created successfully!', 'success')
        return redirect(url_for('main.home'))
        
    return render_template('habit_form.html')

@habit_bp.route('/<int:id>', methods=['GET'])
@login_required
def habit_detail(id):
    """Show habit detail page with check-in option"""
    habit = Habit.query.get_or_404(id)
    
    # Check if habit belongs to current user
    if habit.user_id != current_user.id:
        abort(403)
        
    today = date.today()
    
    # Check if already logged today
    today_log = HabitLog.query.filter_by(
        habit_id=habit.id, 
        date=today
    ).first()
    
    # Get recent logs for history
    recent_logs = HabitLog.query.filter_by(
        habit_id=habit.id
    ).order_by(desc(HabitLog.date)).limit(10).all()
    
    return render_template(
        'habit_detail.html', 
        habit=habit, 
        today_log=today_log,
        recent_logs=recent_logs
    )

@habit_bp.route('/<int:id>/log', methods=['POST'])
@login_required
def log_habit(id):
    """Log a habit completion for today"""
    habit = Habit.query.get_or_404(id)
    
    # Check if habit belongs to current user
    if habit.user_id != current_user.id:
        abort(403)
        
    today = date.today()
    note = request.form.get('note', '')
    
    # Check if already logged today
    existing_log = HabitLog.query.filter_by(
        habit_id=habit.id, 
        date=today
    ).first()
    
    if existing_log:
        # Update note if provided
        if note:
            existing_log.note = note
            db.session.commit()
            flash('Note updated successfully!', 'success')
        else:
            flash('Already logged for today!', 'info')
    else:
        # Create new log
        log = HabitLog(habit_id=habit.id, date=today, note=note)
        db.session.add(log)
        
        # Update streak
        habit.update_streak()
        
        db.session.commit()
        flash('Habit logged successfully!', 'success')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'success': True, 
            'current_streak': habit.current_streak,
            'longest_streak': habit.longest_streak
        })
        
    return redirect(url_for('habit.habit_detail', id=habit.id))

@habit_bp.route('/<int:id>/history', methods=['GET'])
@login_required
def habit_history(id):
    """Show habit history with calendar view"""
    habit = Habit.query.get_or_404(id)
    
    # Check if habit belongs to current user
    if habit.user_id != current_user.id:
        abort(403)
        
    logs = HabitLog.query.filter_by(habit_id=habit.id).order_by(desc(HabitLog.date)).all()
    
    return render_template('habit_history.html', habit=habit, logs=logs)

@habit_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_habit(id):
    """Delete a habit"""
    habit = Habit.query.get_or_404(id)
    
    # Check if habit belongs to current user
    if habit.user_id != current_user.id:
        abort(403)
        
    name = habit.name
    
    db.session.delete(habit)
    db.session.commit()
    
    flash(f'Habit "{name}" deleted successfully!', 'success')
    return redirect(url_for('main.home'))