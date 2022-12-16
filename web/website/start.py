from flask import Flask
from views import views
from auth import auth
from detection import detection


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'rahasia'
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(detection, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
