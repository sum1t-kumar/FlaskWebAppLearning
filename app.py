from flask import Flask, render_template, session
from extensions import debug_toolbar, mail

from common.database import Database
from views.user import users
from views.admin import admin
from models.user.forms import LoginForm


def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    if settings_override:
        app.config.update(settings_override)

    extensions(app)

    @app.before_first_request
    def init_db():
        session['email'] = None
        Database()

    @app.route('/')
    def home_page():
        form = LoginForm()
        return render_template('index.html', form=form)

    app.register_blueprint(users, url_prefix='/user')
    app.register_blueprint(admin, url_prefix='/admin')
    return app


def extensions(app):
    debug_toolbar.init_app(app)
    mail.init_app(app)

    return None


if __name__ == '__main__':
    create_app().run()


