from .main_routes import main_bp
from .habit_routes import habit_bp
from .auth_routes import auth_bp

def register_routes(app):
    """Register all blueprints"""
    app.register_blueprint(main_bp)
    app.register_blueprint(habit_bp, url_prefix='/habit')
    app.register_blueprint(auth_bp, url_prefix='/auth')