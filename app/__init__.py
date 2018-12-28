"""
Contains the application factory and tells Python that this folder should be treated as a package.

"""
import os

from dotenv import load_dotenv
from flask import Flask

def create_app(test_config=None):
    """
    Create and configure the application.
    """
    load_dotenv(verbose=True)
    app = Flask(__name__, instance_relative_config=True)

    # Setup configuration.
    app.config.from_mapping(SECRET_KEY='dev')
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass 

    # Load blueprints. 
    from .auth import auth
    app.register_blueprint(auth)

    return app
 
