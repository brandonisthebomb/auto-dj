"""
Contains the application factory and tells Python that this folder should be treated as a package.

"""
import os, logging

from flask import Flask
from flask.logging import default_handler
from dotenv import load_dotenv

def create_app(test_config=None):
    """
    Create and configure the application.
    """
    # Load environment variables for Flask app.
    load_dotenv(verbose=True)

    # Create application object.
    app = Flask(__name__, instance_relative_config=True)

    # Application configuration.
    if test_config == None: 
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Setup logging.
    root = logging.getLogger()
    root.addHandler(default_handler)  
    root.setLevel(logging.DEBUG)

    # Ensure the instance folder exists.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass 

    # Load blueprints. 
    from autotune.auth import auth
    app.register_blueprint(auth)

    return app
 
