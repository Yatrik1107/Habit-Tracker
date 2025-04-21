from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    habits = db.relationship('Habit', backref='user', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Habit(db.Model):
    __tablename__ = 'habits'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    color = db.Column(db.String(7), default="#3498db")  # Hex color code
    icon = db.Column(db.String(50), nullable=True)
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    logs = db.relationship('HabitLog', backref='habit', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Habit {self.name}>'
    
    def update_streak(self):
        """Update streak based on logs"""
        logs = sorted(self.logs, key=lambda x: x.date, reverse=True)
        
        # No logs yet
        if not logs:
            self.current_streak = 0
            return
            
        # Check if latest log is today
        today = date.today()
        if logs[0].date != today:
            self.current_streak = 0
            return
            
        # Count consecutive days
        streak = 1
        for i in range(len(logs) - 1):
            # If days are consecutive
            if (logs[i].date - logs[i+1].date).days == 1:
                streak += 1
            else:
                break
                
        self.current_streak = streak
        if streak > self.longest_streak:
            self.longest_streak = streak
            
    def is_logged_today(self):
        """Check if habit is logged today"""
        today = date.today()
        return any(log.date == today for log in self.logs)
        
    def is_at_risk(self):
        """Check if habit is at risk of losing streak"""
        yesterday = date.today() - timedelta(days=1)
        return self.current_streak > 0 and not self.is_logged_today()


class HabitLog(db.Model):
    __tablename__ = 'habit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)
    date = db.Column(db.Date, default=date.today)
    note = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<HabitLog {self.habit_id} {self.date}>'