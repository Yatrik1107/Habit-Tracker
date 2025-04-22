from app import create_app

# Create a Flask application instance
app = create_app()

# This 'app' variable will be used by Gunicorn
if __name__ == "__main__":
    app.run()