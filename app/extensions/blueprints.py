from flask_smorest import Api

from app.api.routes.health import blp as health_blp
from app.api.routes.home import blp as home_blp
from app.api.routes.pokemon import blp as pokemon_blp

api = Api()


def init_app(app):
    # initialize flask_smorest api
    api.init_app(app)

    # initialize api blueprints
    api.register_blueprint(home_blp)
    api.register_blueprint(health_blp)
    api.register_blueprint(pokemon_blp)
