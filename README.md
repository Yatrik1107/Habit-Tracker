# Habit Tracker

A modern web application built with Flask to help users track, maintain, and build consistent habits.

**Live Demo:** [https://habit-tracker-0fe0.onrender.com/home](https://habit-tracker-0fe0.onrender.com/home)

## Screenshots


![image](https://github.com/user-attachments/assets/b2794e35-6f88-4fa1-afb2-9a7d52e33156)


## Overview

Habit Tracker is a full-featured web application that allows users to:
- Create and customize habits with different colors and icons
- Track daily habit completions
- Build and maintain streaks
- Add notes to daily check-ins
- View detailed history with calendar visualization

The application focuses on simplicity, visual feedback, and proven psychology principles to help users form lasting habits.

## Features

### User Authentication
- Secure user registration and login
- User profiles with activity summary
- Password hashing for security
- Remember me functionality

### Habit Management
- Create personalized habits with custom colors and icons
- Daily check-ins with optional notes
- Streak tracking with visual indicators
- At-risk warnings when habits haven't been completed

### Visualizations
- Monthly calendar view
- Yearly contribution graph (similar to GitHub's contribution chart)
- Timeline of check-in history
- Current and longest streak statistics

### Modern UI
- Responsive design that works on desktop and mobile
- Clean, intuitive interface with Bootstrap 5
- Visual feedback and animations
- FontAwesome icons for visual cues

## Technology Stack

- **Backend**: Python 3, Flask
- **Database**: SQLAlchemy ORM with SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **CSS Framework**: Bootstrap 5
- **Icons**: Font Awesome 6
- **Authentication**: Flask-Login
- **Deployment**: Gunicorn (WSGI HTTP Server)

## Setup and Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/habit-tracker.git
cd habit-tracker
```

2. Create a virtual environment
```bash
python -m venv venv
```

3. Activate the virtual environment
```bash
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

4. Install dependencies
```bash
pip install -r requirements.txt
```

5. Run the application
```bash
python app.py
```

6. Visit `http://localhost:5000` in your browser

## Project Structure

```
habit-tracker/
├── app.py                # Main Flask application
├── config.py             # Configuration settings
├── models.py             # Database models
├── wsgi.py               # WSGI entry point for production
├── requirements.txt      # Python dependencies
├── static/               # Static files (CSS, JS)
│   └── css/
│       └── main.css      # Custom styles
└── templates/            # HTML templates
    ├── base.html         # Base template with layout
    ├── index.html        # Landing page
    ├── home.html         # User dashboard
    ├── about.html        # About page
    ├── auth/             # Authentication templates
    │   ├── login.html
    │   ├── register.html
    │   └── profile.html
    └── habit_*.html      # Habit-related templates
```

## Future Enhancements

- Email notifications for streak reminders
- Social sharing of achievements
- Challenge mode for habit formation
- Data export and insights
- Dark mode support
- Mobile app integration

## Author

Created by Yatrik Patel

## Acknowledgments

- The "Don't Break the Chain" productivity method by Jerry Seinfeld
- Research on habit formation by James Clear's "Atomic Habits"
- Github's contribution calendar visualization
