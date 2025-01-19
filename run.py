# run.py

from flask import Flask
from app.api.routes import create_routes

def create_app():
    """ 
    Create the Flask app.
        
    """
    app = Flask(__name__)
    create_routes(app) # Create the routes
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)