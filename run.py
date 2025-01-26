from flask import Flask
from app.api.routes import create_routes
def create_app():
    """
    Create the Flask app.
    """
    app = Flask(__name__)
    
    # Import routes from the routes module
    
    # Create the routes
    create_routes(app)
    return app

if __name__ == "__main__":
    try:
        app = create_app()
        app.run(debug=True)
    except Exception as e:
        print(f"An error occurred: {e}")
