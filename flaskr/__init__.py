from . import blog
from . import auth
from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = 'dev'

    app.register_blueprint(auth.bp)

    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
