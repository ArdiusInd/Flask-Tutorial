import os
from flask import Flask

def create_app(test_config=None):
    #  create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # To generate a new secret key: python -c 'import secrets; print(secrets.token_hex())'
    app.config.from_mapping(
        SECRET_KEY='e0e93b077e5a95271ac472c242d6512fd13fc5326422a509b6cda92fef5fd2fa',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    if test_config is None:
        #  Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        #  Load the test config if passed in
        app.config.from_mapping(test_config)

    #  Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #  Import and set up database
    from . import db
    db.init_app(app)

    # Import the Blueptint for auth
    from . import auth
    app.register_blueprint(auth.bp)

    #  Import the Blueprint for the blog
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    
    return app

    #  A simple page that says Hello
    @app.route('/hello')
    def hello():
        return 'Hello, world'
    
    return app