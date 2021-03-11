import os
from flask import Flask

def create_app(config=None):
    # Create the app and configure it
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI="sqlite://",
    )

    if config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
            
    # Import database
    from model.db import db
    db.init_app(app)

    # Add views
    from views.default import default, page_not_found
    from views.prints import prints

    app.register_blueprint(default)
    app.register_blueprint(prints)

    app.register_error_handler(404, page_not_found)

    app.app_context().push()
    db.create_all()

    return app